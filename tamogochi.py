import tkinter as  tk
import sqlite3 
import random


def make_request(query): 
    DB_PATH = r"C:\Users\yarik\OneDrive\Рабочий стол\python folder\bd\tamagochi"
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    connection.close()
    return rows 

def make_request_change(query): 
    DB_PATH = r"C:\Users\yarik\OneDrive\Рабочий стол\python folder\bd\tamagochi"
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()


    

window = tk.Tk()
window.title('tamagochi')
window.geometry('1000x500')

def select_pet(pet_id, pet_name):
    global selected_pet
    selected_pet = pet_id
    selected_label.config(text=f"Выбран питомец: {pet_name}")

def show_stats():   
    for widget in pets_frame.winfo_children():
        widget.destroy()

    pets = make_request("SELECT * FROM pets") 
    for pet_id, name, fullness, mood, health in pets:
        pet_frame = tk.Frame(pets_frame, bd=1, relief="solid", padx=15, pady=15)
        pet_frame.pack(side='left', padx=5)

        tk.Label(pet_frame, text=name).pack()
        tk.Label(pet_frame, text=f'сытость: {fullness}').pack()
        tk.Label(pet_frame, text=f'настроение: {mood}').pack()
        tk.Label(pet_frame, text=f'здоровье: {health}').pack()
        button_select = tk.Button(pet_frame, text="Выбрать", command=lambda pet_id=pet_id, name=name: select_pet(pet_id, name))
        button_select.pack()

def feed_pet():
    global selected_pet
    query = f"""UPDATE pets
            SET fullness = MIN(fullness+10, 100)
            WHERE id = {selected_pet}"""
    make_request_change(query)
    show_stats()

def pet_pet():
    global selected_pet
    query = f"""UPDATE pets
            SET mood = MIN(mood+10, 100)
            WHERE id = {selected_pet}"""
    make_request_change(query)
    show_stats()

def heal_pet():
    global selected_pet
    query = f"""UPDATE pets
            SET health = MIN(health+10, 100)
            WHERE id = {selected_pet}"""
    make_request_change(query)
    show_stats()

def add_pet_window():
    new_window = tk.Tk()
    new_window.title = ('Создание пета') 
    new_window.geometry('1000x500')
    label = tk.Label(new_window, text='напишите имя пета')
    label.pack()
    entry = tk.Entry(new_window)
    entry.pack()
    create_button = tk.Button(new_window, text='создать',command=lambda entry=entry: create_new_pet(entry))
    create_button.pack()

def create_new_pet(entry):
    name = entry.get()
    print(name)
    fullness = random.randint(50, 80)
    mood =  random.randint(40, 68)
    health = random.randint(50, 90)
    query = f"""INSERT INTO pets(name, fullness, mood, health)
            VALUES('{name}', {fullness}, {mood}, {health})"""
    make_request_change(query)

def delete_pet():
    global selected_pet
    query =f"""DELETE FROM pets
                WHERE id = {selected_pet}"""
    make_request_change(query)
    show_stats()
    
def countdown():
    window.after(2000, countdown)
    decrease_mood()
    decrease_fullness()
    decrease_health()
    show_stats()

def decrease_mood():
    query = f"""UPDATE pets
            SET mood = MAX(mood-10, 0)"""                                      
    make_request_change(query)

def decrease_fullness():
    query = f"""UPDATE pets
            SET fullness = MAX(fullness-10, 0)"""                                      
    make_request_change(query)

def decrease_health():
    query = f"""UPDATE pets
            SET health = MAX(health-10, 0)
            WHERE fullness <= 0 or mood <= 0"""                                      
    make_request_change(query)
    death()

def death():
    query = f"""DELETE FROM pets
            WHERE health <= 0""" 
    make_request_change(query)
            


selected_label = tk.Label(window, text='питомец не выбран')
selected_label.pack()

pets_frame = tk.Frame(window)
pets_frame.pack()

button_show_pets = tk.Button(window, text='Показать всех петов', command=show_stats)
button_show_pets.pack()

buttons_frame = tk.Frame(window)
buttons_frame.pack()

button_feed = tk.Button(buttons_frame, text='покормить выбранного пета',command=feed_pet)
button_feed.grid(row=0, column=0, padx=20, pady=10)

button_pet = tk.Button(buttons_frame, text='погладить выбранного пета',command=pet_pet)
button_pet.grid(row=0, column=1, padx=20, pady=10)

button_heal = tk.Button(buttons_frame, text='полечить выбранного пета',command=heal_pet)
button_heal.grid(row=0, column=2, padx=20, pady=10)

open_button = tk.Button(window, text='создать пета', command=add_pet_window)
open_button.pack()

delete_button = tk.Button(window, text='удалить пета', command=delete_pet)
delete_button.pack()

countdown()


window.mainloop()


