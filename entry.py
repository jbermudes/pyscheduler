class Entry:

  def __init__(self, dic, dancers):
    self.entry_id = dic["entry_id"]
    self.act = ""
    self.studio = dic["studio"]
    self.entry_type = "Dance Routine"
    self.category = dic["entry_grouping"]
    self.style = dic["style"]
    self.routine_name = dic["routine_name"]
    self.duration = dic["duration"]
    self.num_dancers = dic["num_dancers"]
    self.level = dic["adj_level"]
    self.age = dic["age_group"]
    self.title = dic["add_title"]
    self.extended = dic["extended"]
    self.adjudication_only = dic["adjudication_only"]
    self.event = dic["event"]
    self.dancers = dancers


  def is_group(self):
    return ("group" in self.category.lower() or "production" in self.category.lower())

  def to_csv(self, delimiter):
    dancers_str = ", ".join(self.dancers)
    s = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"
    s = s.replace(",", delimiter)
    s = s % (
        self.entry_id, self.act, 
        self.routine_name, self.studio,  
        self.age, self.category, self.level,
        self.style,
        self.duration, self.num_dancers, 
        self.title, self.extended, self.adjudication_only,
        self.event, dancers_str)
    return s

  @staticmethod
  def csv_header(delimiter=','):
    s = "entry_id,act,routine_name,studio,age_group,entry_grouping,adj_level," \
        "style,duration," \
        "num_dancers,add_title,extended,adjudication_only,"\
        "event,dancer_roster\n"
    if delimiter != ",":
      s = s.replace(",", delimiter)
    
    return s
  
  def __str__(self):
    s = "Entry Id#%s (%s)" % (str(self.entry_id), str(self.routine_name))
    return s

  def __repr__(self):
    s = "Entry Id#%s" % self.entry_id
    return s

  def __eq__(self, other):
    s1 = set(self.dancers)
    s2 = set(other.dancers)
    intersection = s1.intersection(s2)
    return len(intersection) != 0


