from whoosh.fields import Schema, ID, KEYWORD, TEXT
import io
import os
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.query import Term, And
from whoosh.qparser import QueryParser
import glob


def CreateSchemaInitIndex():
	print "Creating schema"
	my_schema = Schema(id = ID(unique = True, stored = True),\
				path = ID(stored = True),\
				source = ID(stored = True),\
				author = TEXT(stored = True),\
				title = TEXT(stored = True),\
				year = TEXT(stored = True),\
				text = TEXT)
	print my_schema

	if not os.path.exists("gutenbergindex"):
		os.mkdir("gutenbergindex")
	index = create_in("gutenbergindex", my_schema)

def AddDocToIndex(_id, _source, _author, _title, _year):
	index = open_dir("gutenbergindex")
	writer = index.writer()

	print "Creating index {}".format(_id)
	writer.add_document(id = _id,\
				path = _source,\
				source = _source,\
				author = _author,\
				title = _title,\
				year = _year,\
				text = io.open(_source, encoding='utf-8').read())

	writer.commit()

def RunAndPrintQuery(q, index):
	
	searcher = index.searcher()
	results = searcher.search(q)

	print 'Query: {}'.format(q)
	print '#of hits: {}'.format(len(results))
	print 'Best Match: {}'.format(results[0])

def FindFiles():

	count = 0

	for fn in glob.glob("./gutenberg/*.txt"):

		count += 1
	
		with open(fn,'r') as f:
			firstline = f.readline()
			title = find_between_r(firstline,"[","by")
			ay = find_between_r(firstline,"by","]")

			y = [int(s) for s in ay.split() if s.isdigit()]
			al = [s for s in ay.split() if not s.isdigit()]
			author = ' '.join(al)
			year = "0000" 
			if len(y) > 0:
				year = y[0] 
		
		_id = 'guten'+ str(count)

		try:
			AddDocToIndex(unicode(_id, "utf-8",errors='ignore'),\
				unicode(fn, "utf-8",errors='ignore'),\
				unicode(author, "utf-8",errors='ignore'),\
				unicode(title, "utf-8", errors='ignore'),\
				unicode(str(year), "utf-8", errors='ignore'))
		except:
			print "Error on ".format(_id)
			pass
		

def find_between_r( s, first, last ):
	try:
		start = s.rindex( first ) + len( first )
		end = s.rindex( last, start )
		return s[start:end]
	except ValueError:
		return ""


if __name__ == "__main__":

	#CreateSchemaInitIndex()
	#FindFiles()

	index = open_dir("gutenbergindex")

	#perform search tests
	query = And([Term("text","song"), Term("text", "wild")])
	RunAndPrintQuery(query, index)

	parser = QueryParser("text", index.schema)

	query = parser.parse("song wild person")
	RunAndPrintQuery(query, index)

	query = parser.parse("(song OR wild) AND (song OR austen)")
	RunAndPrintQuery(query, index)

	query = parser.parse("song wild author:'William Blake'")
	RunAndPrintQuery(query, index)