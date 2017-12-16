import scholarly

query = "term dependencies | term dependency | term dependence source:SIGIR"
result = scholarly.search_pubs_query(query)

for pub in result:
	article = pub.bib
	print article['title']
	print article['author']
	print 'cited by ' + str(pub.citedby)
