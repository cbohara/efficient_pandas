import pandas as pd

data = pd.read_csv('data/election.csv')
print(data.head())

# add column representing political party
uniq_candidates = data.cand_nm.unique()
parties = {
	'Bachmann, Michelle': 'Republican',
	'Cain, Herman': 'Republican',
	'Gingrich, Newt': 'Republican',
	'Huntsman, Jon': 'Republican',
	'Johnson, Gary Earl': 'Republican',
	'McCotter, Thaddeus G': 'Republican',
	'Obama, Barack': 'Democrat',
	'Paul, Ron': 'Republican',
	'Pawlenty, Timothy': 'Republican',
	'Perry, Rick': 'Republican',
	"Roemer, Charles E. 'Buddy' III": 'Republican',
	'Romney, Mitt': 'Republican',
	'Santorum, Rick': 'Republican'
}
data['party'] = data.cand_nm.map(parties)

# filter out only positive contributions (no refunds)
data = data[data.contb_receipt_amt > 0]

# create sub dataframe representing the top 2 candidates
main_candidates = data[data.cand_nm.isin(['Obama, Barack', 'Romney, Mitt'])]

# determine top contributors to the campaign by occupation
top_ten_contributor_occupations = data.contbr_occupation.value_counts()[:10]

# cleanup vague values
occ_mapping = {
	'INFORMATION REQUESTED PER BEST EFFORTS' : 'NOT PROVIDED',
	'INFORMATION REQUESTED' : 'NOT PROVIDED',
	'INFORMATION REQUESTED (BEST EFFORTS)' : 'NOT PROVIDED',
	'C.E.O.': 'CEO'
}
# if no mapping provided keep original value
data.contbr_occupation = data.contbr_occupation.map(lambda x: occ_mapping.get(x, x))

emp_mapping = {
	'INFORMATION REQUESTED PER BEST EFFORTS' : 'NOT PROVIDED',
	'INFORMATION REQUESTED' : 'NOT PROVIDED',
	'SELF' : 'SELF-EMPLOYED',
	'SELF EMPLOYED' : 'SELF-EMPLOYED',
}
# do the same cleanup for employers
data.contbr_employer = data.contbr_employer.map(lambda x: emp_mapping.get(x, x))

# use pivot table to aggregate data by party and occupation
by_occupation = data.pivot_table('contb_receipt_amt', index='contbr_occupation', columns='party', aggfunc='sum')
