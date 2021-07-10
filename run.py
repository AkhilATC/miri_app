from create_app import create_miri

app = create_miri()
app.run(host='0.0.0.0',port=7001,debug=True)