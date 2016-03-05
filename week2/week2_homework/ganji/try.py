def try_to_make(a_mess):
    try:
        print(1/a_mess)
    except (ZeroDivisionError,TypeError):
        print('ok~')


try_to_make('0')