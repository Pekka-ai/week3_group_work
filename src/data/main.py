from database_manager import DatabaseManager

db_manager = DatabaseManager()

def search_person_and_certificates(name: str):
    rows = db_manager.query_person_by_name(name)
    rows_len = len(rows)
    print()
    if rows_len==1:
        print("löytyi 1 henkilö:")
    elif rows_len==0:
        print("henkilöjä ei löytynyt")
    else:
        print(f"löytyi {rows_len} henkilöä:")
    print()
    for row in rows:
        print_student(row)

def update_person(name:str):
    rows = db_manager.query_person_by_name(name)
    if len(rows)==0:
        print("Henkilöä ei löytynyt.")
    # elif len(rows>1):
    #     print("Löytyi useampi henkilö")
    else:
        
        print("Mitä haluat päivittää? nimi(N), Ikä(I), opiskelijastatus(O)")
        id, name_old, age_old, is_student_old = rows[0]
        try:
            while True:
                command = input("Anna komento: ")
                if command.lower() == 'n':
                    name_new = input("Syötä uusi nimi: ")
                    name_old = name_new
                    break
                elif command.lower() == 'i':
                    while True:
                        try:
                            age_new = int(input("Syötä uusi ikä: "))
                            age_old = age_new
                            break
                        except:
                            print("Anna ikä numeroina")
                    break

                elif command.lower() == 'o':
                    status = input("Onko opiskelija (K/E): ")
                    if status.lower()=='k':
                        is_student_old == True
                    elif status.lower()=='e':
                        is_student_old == False
                    break
        except:
            print("Anna oikeita komentoja..")
                
            
            
        db_manager.update_person(id, name_old, age_old, is_student_old)
        print()
    

def print_student(row: tuple[int, str, int, bool]):
    id, name, age, is_student = row
    status = 'Hän ei ole opiskelija.'
    if is_student:
        status = "Hän on opiskelija."
    print (f"{name}(id: {id}) ja hän on {age} vuotta. {status}")
    certificates = db_manager.query_persons_certificates(id)
    if certificates:
        print("Sertifikaatit:")
        for cert in certificates:
            print(cert[1])
    print()

def add_person():
    while True:
        try: 
            name = input("Anna henkilön nimi: ")
            is_person_in_the_database = db_manager.is_person_in_the_database(name)
            if is_person_in_the_database:
                print("Henkilö on jo tietokannassa")
                break
            age = int(input("Anna henkilön ikä: "))
            student = input("Onko henkilö opiskelija?(K/E) ")
            is_student = False
            if student.lower()=='k':
                is_student = True
            db_manager.insert_person(name, age, is_student)
            print()
            print(f"Henkilö {name} lisättiin onnistuneesti tietokantaan.\n")
            break

        except:
            print("Virhe syötteessä")
        

def main():

    print("\nTällä ohjelmalla voit päivittää henkilötietokantaa\n")
    
    while True:
        try:
            print("0 - Poistu ohjelmasta")
            print("1 - Etsi henkilö")
            print("2 - Päivitä henkilön tietoja")
            print("3 - Lisää henkilö")
            print()
            command = int(input("Valitse toiminto: "))
            
        # print(command)
            if command == 0:
                print("Ohjelma suljetaan.../ns")
                break
            elif command == 1:
                name = input("Syötä nimi")
                search_person_and_certificates(name)
            elif command == 2:
                print("Kenen tietoja haluat päivittää?")
                name = input("Syötä nimi: ")
                update_person(name)
            elif command == 3:
                add_person()
            else:
                print("Anna oikea komento")
        except:
            print("Anna komento numeroilla")


        
main()