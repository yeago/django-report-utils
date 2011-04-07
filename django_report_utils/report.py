from django.utils.datastructures import SortedDict
import copy

class Average(object):
	def __init__(self,x,y):
		self.x = x
		self.y = y

	def __add__(self, other):
		if not self.y:
			return copy.deepcopy(other)

		if not other.y:
			return copy.deepcopy(self)

		new_class = copy.deepcopy(self)
		new_class.x = new_class.x * new_class.y
		new_class.x += (other.x * other.y)
		new_class.y += other.y
		new_class.x = new_class.x / new_class.y # re-average

		return new_class

def get_declared_fields(bases, attrs, with_base_fields=True):
	fields = []
	for field_name, obj in attrs.items():
		try:
			if hasattr(obj,'__metaclass__'):
				fields.append((field_name, attrs.pop(field_name)))
			elif obj.__class__ in [list, dict, Average]:
				fields.append((field_name, attrs.pop(field_name)))

		except AttributeError:
			pass

	return SortedDict(fields)

class ReportOptions(object):
	def __init__(self, options=None):
		self.fields = getattr(options, 'fields', None)
	
class ReportMetaclass(type):
	def __new__(cls, name, bases, attrs):
		fields = get_declared_fields(bases, attrs, True)
		new_class = super(ReportMetaclass, cls).__new__(cls, name, bases, attrs)
		opts = new_class._meta = ReportOptions(getattr(new_class, 'Meta', None))
		new_class.fields = copy.deepcopy(fields)
		return new_class

class Report(object):
	creation_counter = 0
	__metaclass__ = ReportMetaclass
	def __init__(self):
		try:
			for i in self.Meta.fields:
				new_att = Report()
				setattr(self,i,new_att)
				self.fields[i] = new_att

		except AttributeError:
			pass

		for k, v in self.fields.iteritems():
			setattr(self,k,copy.deepcopy(v))

	def __add__(self, other):
		new = copy.deepcopy(self)

		def recurse_and_add(node,node_two):
			for field in node.fields:
				obj = getattr(node,field)
				if isinstance(obj,Report):
					recurse_and_add(obj,getattr(node_two,field))
				elif isinstance(obj,int):
					setattr(node,field,getattr(node,field) + getattr(node_two,field))
				elif isinstance(obj,Average):
					setattr(node,field,getattr(node,field) + getattr(node_two,field))
				elif isinstance(obj,list):
					new_list = []
					for count, i in enumerate(obj):
						if isinstance(i,int):
							new_list.append(obj[count] + getattr(node_two,field)[count])

						if isinstance(i,tuple):
							new_tuple = [] # trust me
							for t_count, t in enumerate(i):
								if not isinstance(t,int):
									new_tuple.append(t)
									continue
								
								new_tuple.append(obj[count][t_count] + getattr(node_two,field)[count][t_count])
							
							new_list.append(tuple(new_tuple))

					setattr(node,field,new_list)
					
			return node

		return recurse_and_add(new, other)
