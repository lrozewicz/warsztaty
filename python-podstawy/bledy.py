try:
    wynik = 10 / 0
except ZeroDivisionError:
    print("Nie można dzielić przez zero!")
finally:
    print("Blok finally zawsze się wykona.")
