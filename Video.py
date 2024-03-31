class Video:

    def __init__(self,path,size,type,name,ext):
        self.path = path
        self.size = size
        self.type = type
        self.name = name
        self.ext = ext

    def delete(self):#deletes the file
        self.path.unlink()



