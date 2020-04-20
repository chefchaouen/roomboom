import re

def main():
	
	text = '1.9万円'
	
	match = re.search('[0-9]', text).group(0)

	print(match)

if __name__=='__main__':
	main()
