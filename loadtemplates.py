def loadTemplates(names):
	temps = dict()

	for temp in names:
		with open ("html/subsections/" + temp + ".html", "r") as file:
			temps[temp] = file.read()

	return temps