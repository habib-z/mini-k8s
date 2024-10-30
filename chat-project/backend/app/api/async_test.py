import asyncio
import time


async def func1():
    print('func1 start')
    await asyncio.sleep(4)
    print('func1 end')

async def func2(num):
    print(f'func2 start {num}')
    await asyncio.sleep(2)
    print(f'func2 end {num}')
    return num

def func3():
    print ('func3 start')
    print ('func3 end')
async def main():
    # print('start main')
    f1co= func1()
    print(f'type of f1co= {type(f1co)}')
    print('after coroutine func1 created')
    c1 = asyncio.create_task(f1co)

    print('after creating c1')
    f2co = func2(1)
    c2 = asyncio.create_task(f2co)
    time.sleep(10)
    # r1=await c1
    print('between')
    c2=asyncio.create_task(func2(2))
    print('after creating c2')
    #print(f"result of await c2={await c2}")
    print('between c2s')
   # print(r2)
   # r3=await c2
   # print(r3)
    print('finish both')

if __name__ == '__main__':
    asyncio.run(main())

