from app.database import SessionLocal, engine, Base
from app.models.dog import Dog, Sex as DogSex
from app.models.cat import Cat, Sex as CatSex
import app.models.dog  # noqa: F401
import app.models.cat  # noqa: F401

Base.metadata.create_all(bind=engine)

dogs = [
    Dog(name="Max",    breed="Labrador Retriever", age=3.0, weight=30.0, sex=DogSex.macho,  owner="Carlos Pérez"),
    Dog(name="Luna",   breed="Beagle",             age=2.0, weight=12.5, sex=DogSex.hembra, owner="Ana García"),
    Dog(name="Rocky",  breed="Bulldog Francés",    age=4.0, weight=11.0, sex=DogSex.macho,  owner="Luis Torres"),
    Dog(name="Coco",   breed="Poodle",             age=1.5, weight=8.0,  sex=DogSex.hembra, owner="María López"),
    Dog(name="Thor",   breed="Pastor Alemán",      age=5.0, weight=35.0, sex=DogSex.macho,  owner="José Martínez"),
    Dog(name="Nala",   breed="Labrador Retriever", age=2.5, weight=27.0, sex=DogSex.hembra, owner="Laura Sánchez"),
    Dog(name="Buddy",  breed="Golden Retriever",   age=6.0, weight=32.0, sex=DogSex.macho,  owner="Pedro Ramírez"),
    Dog(name="Lola",   breed="Chihuahua",          age=3.0, weight=2.5,  sex=DogSex.hembra, owner="Sofía Díaz"),
    Dog(name="Simba",  breed="Rottweiler",         age=4.5, weight=45.0, sex=DogSex.macho,  owner="Diego Flores"),
    Dog(name="Bella",  breed="Poodle",             age=1.0, weight=7.5,  sex=DogSex.hembra, owner="Valentina Cruz"),
    Dog(name="Duke",   breed="Beagle",             age=3.5, weight=13.0, sex=DogSex.macho,  owner="Andrés Moreno"),
    Dog(name="Canela", breed="Golden Retriever",   age=2.0, weight=28.5, sex=DogSex.hembra, owner="Gabriela Ruiz"),
]

cats = [
    Cat(name="Michi",   breed="Siamés",            age=2.0, weight=4.0,  sex=CatSex.macho,  owner="Carlos Pérez"),
    Cat(name="Misu",    breed="Persa",             age=3.0, weight=5.5,  sex=CatSex.hembra, owner="Ana García"),
    Cat(name="Nube",    breed="Angora Turco",      age=1.5, weight=3.8,  sex=CatSex.hembra, owner="Luis Torres"),
    Cat(name="Oliver",  breed="Maine Coon",        age=4.0, weight=7.0,  sex=CatSex.macho,  owner="María López"),
    Cat(name="Salem",   breed="Bombay",            age=5.0, weight=4.5,  sex=CatSex.macho,  owner="José Martínez"),
    Cat(name="Luna",    breed="Siamés",            age=2.5, weight=3.5,  sex=CatSex.hembra, owner="Laura Sánchez"),
    Cat(name="Gatito",  breed="Ragdoll",           age=1.0, weight=6.0,  sex=CatSex.macho,  owner="Pedro Ramírez"),
    Cat(name="Cleo",    breed="Persa",             age=3.5, weight=5.0,  sex=CatSex.hembra, owner="Sofía Díaz"),
    Cat(name="Whisky",  breed="Maine Coon",        age=6.0, weight=8.5,  sex=CatSex.macho,  owner="Diego Flores"),
    Cat(name="Dulce",   breed="Ragdoll",           age=2.0, weight=5.5,  sex=CatSex.hembra, owner="Valentina Cruz"),
    Cat(name="Tigre",   breed="Bengalí",           age=4.0, weight=5.0,  sex=CatSex.macho,  owner="Andrés Moreno"),
    Cat(name="Perla",   breed="Bengalí",           age=1.5, weight=3.2,  sex=CatSex.hembra, owner="Gabriela Ruiz"),
]

db = SessionLocal()
try:
    db.add_all(dogs)
    db.add_all(cats)
    db.commit()
    print(f"{len(dogs)} perros insertados correctamente.")
    print(f"{len(cats)} gatos insertados correctamente.")
finally:
    db.close()
