#include <stdio.h>
#include <stdlib.h>		
#include <string.h>		//包含bzero等函数
#include <unistd.h>

#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <netinet/ip_icmp.h>
#include <signal.h>
#include <arpa/inet.h>
#include <errno.h>
#include <sys/time.h>
#include <netdb.h>
#include <pthread.h>

//宏定义
//icmp类型
#define ICMP_ECHO 8
#define ICMP_REPLY 0
//icmp头部长度
#define ICMP_HEADER_LEN 8
//发送队列长度（未接收到任何包时最多发送的包数量）
#define SEND_LINE_MAX 10
//ICMP数据部分的最大长度
#define ICMP_DATA_MAX 1024
//默认ICMP数据部分长度，未在参数中指定长度时使用
#define ICMP_DEFAULT_DATA_LEN 36
//打印更多信息用于debug
#define DEBUG

//icmp echo包格式
typedef struct icmp_echo
{
    u_int8_t type;
    u_int8_t code;
    u_int16_t cksum;
    u_int16_t pid;
    u_int16_t seq;
    u_int8_t data[ICMP_DATA_MAX];
    
}ICMP_ECHO_t;

//记录已发送的包的格式
typedef struct package_info{
    struct timeval send_time;
    int seq;
    int flag;
}PACKAGE_INFO_t;

typedef struct timeval TIMEVAL_t;
typedef struct sockaddr_in SOCK_ADDR_IN_t;

//全局变量
//标志程序是否执行结束，用来和发送/接收线程同步
int g_process_active = 0;
//当前进程pid
int g_pid = 0;
//已发送的包数量
int g_package_sended = 0;
//当前进程pid接收的包数量
int g_package_recved = 0;
//发送和接收用的socket
int g_sockfd = -1;
//icmp数据长度
int g_icmp_data_len = ICMP_DEFAULT_DATA_LEN;
//程序启动和结束时间
TIMEVAL_t g_process_begin, g_process_end;
//记录已发送包的信息
PACKAGE_INFO_t g_sended_package[SEND_LINE_MAX] = { 0 };
//目标地址
SOCK_ADDR_IN_t g_dest_addr;


//计算两个时间点之间的时间间隔
TIMEVAL_t calculateInterval(TIMEVAL_t begin, TIMEVAL_t end){
    TIMEVAL_t interval;
    interval.tv_sec = end.tv_sec - begin.tv_sec;
    interval.tv_usec = end.tv_usec - begin.tv_usec;
    if(interval.tv_sec < 0){
        interval.tv_sec--;
        interval.tv_usec += 1000000;
    }
    return interval;
}

//通过序号获取发送队列中的包（或者找到空位置）
PACKAGE_INFO_t* getPackageBySeq(int seq){
    int i;
    //seq为-1则找一个空闲位置（flag=0的位置）,否则在flag=1的包中查找该seq的包
    if(seq == -1){
        for(i=0; i<SEND_LINE_MAX; i++){
            if(g_sended_package[i].flag == 0){
                return &g_sended_package[i];
            }
        }
    }else{
        for(i=0; i<SEND_LINE_MAX; i++){
            if(g_sended_package[i].seq == seq && g_sended_package[i].flag == 1){
                return &g_sended_package[i];
            }
        }
    }
    return NULL;
}

//打印出发送队列，调试中
void checkSendLine(){
    int i;
    for(i=0; i<SEND_LINE_MAX; i++){
        printf("ordinal:%d, seq:%d, flag:%d\n", i, g_sended_package[i].seq, g_sended_package[i].flag);
    }
}
//计算校验和
int cksum(void* data, int len)
{
    int i;
    int is_odd;
    int sum=0;
    //用长度为奇数时处理最后一个16bit
    u_int16_t last;
    
    is_odd = len & 0x1;
    int add_times = len >> 1;
    u_int16_t* p = (u_int16_t*)data;

    for(i=0;i<add_times;i++){
        sum += *p;
        p++;
    }

    //最后8bit补充8bit的0构成16bit参与计算
    //计算校验和时的16bit是小端编址（低位低地址，高位高地址）
    if(is_odd == 1){
        last = *(u_int8_t*)p & 0xff;
        sum += last;
    }

    sum = (sum >> 16) + (sum & 0xffff);
    sum += (sum >> 16);
    return ~sum;

}

void icmp_pack(ICMP_ECHO_t* icmp_package, int seq, int pid, int data_len)
{//构造icmp请求包
    icmp_package->type = ICMP_ECHO;
    icmp_package->code = 0;
    icmp_package->cksum = 0;
    icmp_package->seq = seq;
    icmp_package->pid = pid;
    //填充数据部分
    memset(icmp_package->data, 0xff, data_len);
    //计算校验和
    icmp_package->cksum = cksum(icmp_package, data_len + ICMP_HEADER_LEN);
}

//解析收到的数据包，打印相关信息icmp，设置发送队列对应包的状态，调整接收到包的数量
void icmp_unpack(void* buf, int len, TIMEVAL_t recv_time){
    int ip_header_len;
    int icmp_len;
    struct ip* ip = NULL;
    ICMP_ECHO_t* icmp = NULL;
    PACKAGE_INFO_t* pk = NULL;
    TIMEVAL_t interval;
    float rtt;
    //解析ip头部和icmp头部
    ip = (struct ip*)buf;
    ip_header_len = ip->ip_hl * 4;
    icmp = (ICMP_ECHO_t*)(buf + ip_header_len);
    icmp_len = len - ip_header_len;

    if(icmp_len < 8){
        printf("bad icmp package\n");
    }
    if((icmp->type == ICMP_REPLY) && (icmp->pid == g_pid)){
        pk = getPackageBySeq(icmp->seq);
        if(pk != NULL){
            pk->flag = 0;
            //收到一个回复包，收到的包计数加一
            g_package_recved++;
            
            //计算延迟并打印信息
            interval = calculateInterval(pk->send_time, recv_time);
            rtt = (float)(interval.tv_sec * 1000) + (float)(interval.tv_usec) / 1000;
            printf("%d bytes from %s: icmp_seq=%u ttl=%d rtt=%.2f ms\n",
                len,
                inet_ntoa(ip->ip_src),
                icmp->seq,
                ip->ip_ttl,
                rtt);

        }else{
                printf("recv unknow icmp package\n");
#ifdef DEBUG
                printf("seq is %d\n", icmp->seq);
                checkSendLine();
#endif

        }
    }
}

//发送数据包
void* icmp_send(void* para){
    int pk_size = sizeof(ICMP_ECHO_t) - ICMP_DATA_MAX + g_icmp_data_len;
    ICMP_ECHO_t icmp_package;
    PACKAGE_INFO_t* pk;
    gettimeofday(&g_process_begin, NULL);
    while(g_process_active){
        //构造icmp echo包（包头和数据）
        icmp_pack(&icmp_package, g_package_sended, g_pid, g_icmp_data_len);
        //在已发送队列里找到空位
        pk = getPackageBySeq(-1);
        if(pk != NULL){
            //记录发送icmp的信息
            gettimeofday(&(pk->send_time), NULL);
            pk->seq = g_package_sended;
            //准备发送时将发送队列中分配的该位置设置为待接收状态，若发送失败再改回空闲状态
            pk->flag = 1;
            if(sendto(g_sockfd, &icmp_package, pk_size, 0, (struct sockaddr*)&g_dest_addr, sizeof(g_dest_addr)) < 0){
                printf("error when sending package %d\n", g_package_sended);
                //发送失败，将该位置改回空闲状态
                pk->flag == 0;
            }else{
                //发送成功后记录该包为待接收状态，将已发送的包数量加1
                g_package_sended++;
            }
        }else{
            //发送队列已满则停止发送
            printf("packages sended up to max\n");
            return NULL;
        }
        sleep(1);
    }
    return NULL;
}

//接收回应
void* icmp_recv(void* para){
    //接收到的数据大小
    int size;
    //接收时间
    TIMEVAL_t recv_time;
    //缓冲区
    int recv_buff[10240];
    //select的超时时间
    TIMEVAL_t interval;
    //设置为1ms
    interval.tv_sec = 0;
    interval.tv_usec = 1000;
    //
    fd_set  readfd;
    
    int result = 0;
    while(g_process_active){
		FD_ZERO(&readfd);
		FD_SET(g_sockfd, &readfd);
        //检测是否有数据可接收(使用select是为了能够定时检查g_proces_active的状态，从而能正常退出程序)
		result = select(g_sockfd+1,&readfd, NULL, NULL, &interval);
        switch(result){
            case -1:
                perror("Error when waiting reply");
                break;
            case 0:
                break;
            default:
                 /*接收数据*/
                size = recv(g_sockfd, recv_buff,sizeof(recv_buff), 0);
                if(size < 0)
                {
                    perror("recv error");
                    continue;
                }
                gettimeofday(&recv_time, NULL);
                /*解包，并设置相关变量*/
                icmp_unpack(recv_buff, size, recv_time);
        }
       
    }
    return NULL;
}

//打印发送和接收的icmp包数量，丢包率，程序运行时间等等
void statistics(){
    TIMEVAL_t interval;
    int interval_ms;
    float lost_package_rate;
    if(g_package_sended != 0){
        lost_package_rate = ((float)(g_package_sended - g_package_recved) / (float)g_package_sended) * 100;
    }else{
        lost_package_rate = 0;
    }
        
    interval = calculateInterval(g_process_begin, g_process_end);
    interval_ms = interval.tv_sec * 1000 + interval.tv_usec / 1000;
    printf("\n%d packages sended, %d packages received, %.2f%% lost\n", g_package_sended, g_package_recved, lost_package_rate);
    printf("process end, duration %dms\n", interval_ms);
}

//接收ctrl+c信号，记录程序结束时间，通知发送和接收线程结束
void icmp_sigint(){
    g_process_active = 0;
    gettimeofday(&g_process_end, NULL);
}

//显示如何使用该程序
void ping_usage_info(){
    printf("Invalid arguments, try again as follow:\n");
    printf("ping [-s len] xx.xx.xx.xx\n");
    printf("MAX len is 1024\n");
}

int main(int argc, char* argv[]){
    const char* input_addr;
    struct hostent* host = NULL;
    struct protoent* protocol = NULL;
    u_int32_t inaddr = INADDR_NONE;
    int size = 128 * 1024;
    //读取参数
    if(argc < 2){
        ping_usage_info();
        return 0;
    }
    if(strcmp(argv[1], "-s") == 0 && argc == 4){
        g_icmp_data_len = atoi(argv[2]);
        if(g_icmp_data_len > 1024){
            printf("The len is too large, try smaller one\n");
            return 0;
        }
        input_addr = argv[3];

    }else if(argc == 2){
        input_addr = argv[1];
    }else{
        ping_usage_info();
        return 0;
    }

    //获取icmp协议的编号，在创建socket时使用
    protocol = getprotobyname("icmp");
    if(protocol == NULL){
        perror("get protocol name error");
        return -1;
    }

    g_pid = getpid();
    printf("current pid is %d\n", g_pid);

    //创建socket
    g_sockfd = socket(PF_INET, SOCK_RAW, protocol->p_proto);
    if(g_sockfd < 0){
        perror("create socket error");
        return -1;
    }
    //给系统设置更大的接收缓冲区
    setsockopt(g_sockfd, SOL_SOCKET, SO_RCVBUF, &size, sizeof(size));
    //填充目的地址结构sockaddr_in
    bzero(&g_dest_addr, sizeof(g_dest_addr));
    g_dest_addr.sin_family = AF_INET;
	inaddr = inet_addr(input_addr);
	if(inaddr == INADDR_NONE){
		//输入的是域名
		host = gethostbyname(input_addr);
		if(host == NULL){
			perror("get host ip error");
			return -1;
		}
		//将地址复制到dest中
		memcpy(&g_dest_addr.sin_addr, host->h_addr, host->h_length);
	}else{
        //将地址复制到dest中
		memcpy(&g_dest_addr.sin_addr, &inaddr, sizeof(inaddr));
	}

    //打印发送参数的提示
    inaddr = g_dest_addr.sin_addr.s_addr;
	printf("PING %s (%ld.%ld.%ld.%ld) %d(%d) bytes of data.\n", 
		input_addr, 
		(inaddr&0x000000FF)>>0,
		(inaddr&0x0000FF00)>>8,
		(inaddr&0x00FF0000)>>16,
		(inaddr&0xFF000000)>>24,
        g_icmp_data_len,
        g_icmp_data_len + 28);
    
    //截取信号SIGINT
	signal(SIGINT, icmp_sigint);

    //启动发送和接收线程
	g_process_active = 1;						
	pthread_t send_id, recv_id;		
	if(pthread_create(&send_id, NULL, icmp_send, NULL) < 0){
        perror("send thread create error");
		return -1;
	}
	if(pthread_create(&recv_id, NULL, icmp_recv, NULL) < 0){
        perror("receive thread create error");
		return -1;
	}
	
	/*等待线程结束*/
	pthread_join(recv_id, NULL);
    pthread_join(send_id, NULL);
	/*清理并打印统计结果*/
	close(g_sockfd);
	statistics();
	return 0;	
}