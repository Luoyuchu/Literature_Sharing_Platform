import os
import datetime
import modules

app = modules.create_app()
app.config['JSON_AS_ASCII'] = False
app.config['MONGO_URI'] = 'mongodb://localhost:27017'
# app.config['MONGO_DATABASE'] = 'vispub'
app.config['MONGO_DATABASE'] = 'test'
app.config['MONGO_AUTH_COLLECTION'] = 'auth'
app.config['MONGO_PAPER_COLLECTION'] = 'paper'
app.config['MONGO_NOTE_COLLECTION'] = 'note'
app.config['MONGO_RATING_COLLECTION'] = 'rating'
app.config['MONGO_ANNOTATION_COLLECTION'] = 'annotation'
app.config["PAPER_PATH"] = os.path.abspath("./paper")
app.config['SECRET_KEY'] = "asdgqer4yhadfert243557u1fasdfhj56qdgdgsjhsfgasgsdf"
app.config['EXPIRE_DURATION'] = datetime.timedelta(hours=4)

if __name__ == "__main__":
    app.run(debug=True)
