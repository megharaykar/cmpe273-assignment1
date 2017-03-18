from flask import Flask
import sys,base64
from github import Github
app = Flask(__name__)
outputstring=""
@app.route("/")
def hello():
	output=outputstring.replace("\n","<br>")
	return output

if __name__ == "__main__":
	try:
		arg1 = sys.argv[1]
		val,repositoryurl=arg1.split("https://github.com/")
		user,reponame=repositoryurl.split("/")
		github = Github()
		repository = github.get_user(user).get_repo(reponame)
		list_of_files=repository.get_dir_contents('')
		for file in list_of_files:
			filepath = file.path
			if filepath.endswith("config.yml") or filepath.endswith("config.json"):
				print(filepath)
				file_content = repository.get_contents(filepath)
				file_data = base64.b64decode(file_content.content)
				outputstring=outputstring+file_data
				print(file_data)
		print("The Final output is \n")
		print(outputstring)
		app.run(debug=False,host='0.0.0.0')
	except IndexError:
		print("Usage: app.py <arg1>")
		sys.exit(1)