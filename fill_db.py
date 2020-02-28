from app.main import create_app
from app.models import AnimalCenter

app = create_app()

with app.app_context():

    user = AnimalCenter(login='ann', address='lp')
    user.set_password('a')
    app.db.session.add(user)
    user = AnimalCenter(login='a', address='lp')
    user.set_password('a')
    app.db.session.add(user)
    app.db.session.commit()
    app.db.engine.execute('insert into species(name, description, price)'
                          'values("cat", "good cat", 160),'
                                '("dog", "good dog", 300),'
                                '("fox", "perfect fox", 200)')
    app.db.engine.execute('insert into animal(center_id, name, description, age, species_id, price)'
                          ' values(1, "toto", "t", 3, 1, 100),'
                                 '(2, "momo", "m", 2, 1, 170),'
                                 '(1, "lolo", "l", 10, 3, 100),'
                                 '(1, "jojo", "j", 2, 1, 289)')