import time
from apscheduler.schedulers.blocking import BlockingScheduler




# 1분 10초마다 실행
def exec_cron():
    print(f'job1: {time.strftime("%H : %M : %S")}')
    f = open('libs/recommendation/get_train_insert.py', encoding='utf-8')
    exec(f.read(), globals())
    # f.close()


if __name__ == '__main__':
    sched = BlockingScheduler(daemon=True)  # deamon : flask를 종료할 떄 스레드 종료 가능

    # 매일 오후 23시 59분에 실행
    # sched.add_job(exec_cron, 'cron', hour=23, minute=59)
    sched.add_job(exec_cron, 'cron', hour=14, minute=45)

    print('sched before ~')
    sched.start()
    time.sleep(5)
    print('sched after ~')