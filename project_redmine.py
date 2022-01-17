from redminelib import Redmine
import datetime
import argparse


projects=["hapee","aloha","packetshield" ,"licserv" ,"bootstrap"] # "documentation", 

def groupBy(year, issues):
    #global issues
    start_date=datetime.date(year,1,1)
    end_date=datetime.date(year,12,31)

    a={"total":0}
    #print( len(issues ) )
    status=set( [i.status.name for i in issues  ] )
    for n in status:
        _ = [ n for i in issues \
                if "start_date" in i.__dir__() and start_date < i.start_date < end_date \
                and i.status.name == n ]

                #if i.status.name==s ]
        #_ = [i for i in issues if start_date < i.start_date < end_date ]
        a[n]=len(_) #.append({s:len(_)} )
        a["total"]+=a[n]

    return a



class MyParser(argparse.ArgumentParser):
    """A parser that displays argparse's help message by default."""

    def error(self, message):
        self.print_help()


class MyClass:

    apikey=""
    project=""
    output="issues_%s.txt"
    sep=";"

    #def __init__(self):
    def argparse(self):
        self.parser = MyParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

        self.parser.add_argument("-a", "--apikey", default="", help="""apikey for redmine""")
        self.parser.add_argument("-p", "--project", default="hapee", help="""one of [ hapee | packetshield | documentation | licserv | bootstrap ] """)
        self.parser.add_argument("-o", "--output", default="issues_%s.txt", help="""output filename""")
        self.parser.add_argument("-s", "--sep", default="\t", help="""separator""")

        self.parse()
        return self

    def parse(self):
        args = self.parser.parse_args()
        self.sep = args.sep
        self.output = args.output
        self.project = args.project
        filename = args.output % args.project


    def years(start_year=2015,end_year=2022, issues={}, sep="\t" ):
        years={}
        for year in range(2015,2022+1):
            years[year]=groupBy(year, issues)

        mx=len(str(years[year]))
        keys=years[year].keys()

        def clr(a):
            return a
            return a.replace(" ","").lower()

        line= sep.join( ["{%s:>%i}"%(clr(k),len(k)if sep=="\t" else 0) for k in keys ] )
        header="year"+sep+"{}\n".format(line.format(**{k:k for k in keys} ) )
        output=header
        for year in years:
            o=""
            results=years[year]
            output +="{}{}{}\n".format(year, sep, line.format( **results ) )

        return {'output':output,'results':results}

    def connect(self):
        self.redmine = Redmine('https://redmine.int.haproxy.com', output=self.output, apikey=self.apikey)

    def main(self):
        #args = self.parser.parse_args()
        self.connect()
        if self.project == 'all':
            self.get_all()
        else:
            self.get(self.project,title=self.project)

    def get_all(self):
        for p in projects:
            self.get(p,title=p)



    def get(self,p,title=""):
        redmine = self.redmine

        project = redmine.project.get(p)

        filename = self.output % self.project

        self.issues=project.issues

        status=set( [i.status.name for i in self.issues  ] )
        projects= [ p.name for p in redmine.project.all() ]
        #print( status)
        out = self.years(issues=self.issues,sep=self.sep)
        open(filename,'a+').write(f"{title}\n"+out['output'])

if __name__ == '__main__':
    c=MyClass()
    c.argparse().main()

