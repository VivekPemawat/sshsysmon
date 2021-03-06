from .timespan import TimeSpan
from .size import ByteSize
from datetime import datetime
from dateutil.parser import parse

# Merge b into a. path is for logging
def merge(a, b, path=[], overwrite=False):
	o = dict(a) # Clone

	for key in b:
		if key in o:
			if isinstance(o[key], dict) and isinstance(b[key], dict):
				o[key] = merge(o[key], b[key], path + [str(key)], overwrite)
			elif o[key] == b[key]:
				pass # Same node
			elif overwrite:
				o[key] = b[key]
			else:
				raise Exception("Conflict at '%s'" % '.'.join(path + [str(key)]))
		else:
			o[key] = b[key]
	return o

# given a path such as a.b.[3]
# resolve what is in the object at that location, or default
def find(obj, path, default = None):
	paths = path.split('.')

	try:
		ret = obj
		for k in paths:
			if not k:
				continue
			elif k.startswith('[') and k.endswith(']'):
				# numeric
				ret = ret[int(k[1:-1])]
			else:
				ret = ret[k]

		return ret
	except:
		return default

# Given the format "path:type", where type is one listed below
# resolve the value of the object at the given path to the required type
def findTyped(obj, path, default = None):
	decl = path.split(':')
	objPath = decl[0]
	objType = decl[1] if len(decl) >= 2 else None

	resolved = find(obj, objPath, default)

	try:
		if objType == 'str':
			return str(resolved)
		if objType == 'int':
			return int(resolved)
		if objType == 'ByteSize':
			return ByteSize(int(resolved))
		if objType == 'TimeSpan':
			return TimeSpan(int(resolved))
		if objType == 'TimeSpanFromNow':
			return TimeSpan((datetime.now() - parse(resolved).replace(tzinfo=None)).total_seconds())
		if objType == 'DateTime':
			return parse(resolved)
	except Exception as e:
		pass

	return resolved
