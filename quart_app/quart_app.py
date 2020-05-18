from quart import Quart, render_template
import pymysql as sql
import os
import random


images = [
    "https://firebasestorage.googleapis.com/v0/b/docker-curriculum.appspot.com/o/catnip%2F0.gif?alt=media&token=0fff4b31-b3d8-44fb-be39-723f040e57fb",
    "https://firebasestorage.googleapis.com/v0/b/docker-curriculum.appspot.com/o/catnip%2F1.gif?alt=media&token=2328c855-572f-4a10-af8c-23a6e1db574c",
    "https://firebasestorage.googleapis.com/v0/b/docker-curriculum.appspot.com/o/catnip%2F10.gif?alt=media&token=647fd422-c8d1-4879-af3e-fea695da79b2",
    "https://firebasestorage.googleapis.com/v0/b/docker-curriculum.appspot.com/o/catnip%2F11.gif?alt=media&token=900cce1f-55c0-4e02-80c6-ee587d1e9b6e",
    "https://firebasestorage.googleapis.com/v0/b/docker-curriculum.appspot.com/o/catnip%2F2.gif?alt=media&token=8a108bd4-8dfc-4dbc-9b8c-0db0e626f65b",
    "https://firebasestorage.googleapis.com/v0/b/docker-curriculum.appspot.com/o/catnip%2F3.gif?alt=media&token=4e270d85-0be3-4048-99bd-696ece8070ea",
    "https://firebasestorage.googleapis.com/v0/b/docker-curriculum.appspot.com/o/catnip%2F4.gif?alt=media&token=e7daf297-e615-4dfc-aa19-bee959204774",
    "https://firebasestorage.googleapis.com/v0/b/docker-curriculum.appspot.com/o/catnip%2F5.gif?alt=media&token=a8e472e6-94da-45f9-aab8-d51ec499e5ed",
    "https://firebasestorage.googleapis.com/v0/b/docker-curriculum.appspot.com/o/catnip%2F7.gif?alt=media&token=9e449089-9f94-4002-a92a-3e44c6bd18a9",
    "https://firebasestorage.googleapis.com/v0/b/docker-curriculum.appspot.com/o/catnip%2F8.gif?alt=media&token=80a48714-7aaa-45fa-a36b-a7653dc3292b",
    "https://firebasestorage.googleapis.com/v0/b/docker-curriculum.appspot.com/o/catnip%2F9.gif?alt=media&token=a57a1c71-a8af-4170-8fee-bfe11809f0b3",
]


app = Quart(__name__)


def get_connection():
    # here we get variables from system's Environment
    return sql.connect(host='mysql',
                       user=os.environ['MYSQL_USER'],
                       passwd=os.environ['MYSQL_PASSWORD'],
                       db=os.environ['MYSQL_DATABASE'],
                       charset='utf8mb4',
                       autocommit=True)


@app.route("/", methods=['GET'])
async def index():
    url = random.choice(images)
    return await render_template("index.html", url=url)


@app.route("/dump", methods=['GET'])
async def mysqldump():
    private_db = "/quart_database/private"
    # in container's filesystem
    # in host filesystem it is ../service_example/storage/private

    try:
        conn = get_connection()
        with conn:
            cur = conn.cursor()
            with cur:
                cur.execute("USE users_db; ")
                # we can use f"USE {os.environ['MYSQL_DATABASE']}"
                # but it is unsafe
                # "USE %s; " doesnt work here

                query = "SELECT * FROM users WHERE mark > %s LIMIT 3; "
                args = (2, )
                cur.execute(query, args)

                good_users = '\n'.join(str(user) for user in cur.fetchall())
                with open(f"{private_db}/users.txt", "w") as file:
                    file.write(good_users)

    except Exception as e:
        with open(f"{private_db}/errors.txt", "a") as errfile:
            errfile.write(str(e))
            raise(e)
            return str(e)

    else:
        return 'look for a new file in private_db'


@app.route('/testing', methods=['GET'])
async def test():
    return 'Testing'


def main():
    # do not use it in deploy
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


if __name__ == '__main__':
    main()
