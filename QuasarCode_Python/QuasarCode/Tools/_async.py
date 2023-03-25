from asyncio import get_event_loop

def start_main_async(main_function, *args, **kwargs):
    loop = get_event_loop()
    loop.run_until_complete(main_function(*args, **kwargs))
