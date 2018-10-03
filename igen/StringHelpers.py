# coding=utf-8

def lower_first_letter(st):
	return st[0].lower() + st[1:]

def upper_first_letter(st):
	return st[0].upper() + st[1:]

def snake_to_camel(st):
    components = st.split('_')
    return components[0] + "".join(x.title() for x in components[1:])

def plural_to_singular(st):
	if st.endswith("ies"):
		if len(st) > 3:
			if st[-4] not in "aeiou":
				return st[0:-3] + "y"
	elif st.endswith("es"):
		if st[-3] in "sxo":
			return st[0:-2]
		elif st[-4:-2] == "ch" or st[-4:-2] == "sh":
			return st[0:-2]
		else:
			return st[0:-1]
	elif st.endswith("s"):
		if len(st) > 3:
			return st[:-1]
	return st