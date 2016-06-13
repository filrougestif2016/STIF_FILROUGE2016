# -*- coding: utf-8 -*-
import os
from optparse import OptionParser
import stif_nexterite_properties
import codecs
logger = stif_nexterite_properties.logger

def select_impact(infilename, str_date):
    selected_lines = []
    with codecs.open(infilename, 'r', encoding="iso-8859-1") as f:
        lines = f.readlines()
    logger.debug("select_impact %s %d lines"%(infilename,len(lines)))
    for line in lines:
        tokens= line.split(';')
        if len(tokens) > 0:
            try :
                if tokens[1].startswith(str_date):
                    selected_lines.append(line)
            except IndexError:
                logger.error("select_impact invalid format %s"%line)
    return selected_lines

def extract_impact(csv_lines):
    new_lines = []
    for row in csv_lines:
        tokens = row.split(';')
        try :
            new_lines.append(' '.join([tokens[3],tokens[4]]))
        except IndexError:
            logger.error("extract_impact invalid format %s"%row)
    return new_lines

def write_impact(select_date,dir=None):
    data_dir=stif_nexterite_properties.data_impact_dir
    impact_filename = data_dir +stif_nexterite_properties.impact_file_name
    selected_lines = select_impact(impact_filename,select_date)
    if dir==None:
        dir = stif_nexterite_properties.data_impact_dir
    ftt = codecs.open(os.path.join(dir, 'IMPACT_'+select_date+'.csv'), 'wb',encoding="iso-8859-1")
    joined_lines = extract_impact(selected_lines)
    for line in joined_lines:
        ftt.write(line)
    ftt.close()
    lines_count = len(joined_lines)
    logger.info("IMPACT_"+select_date+" %d"%(lines_count))
    return lines_count

if __name__ == '__main__' :
    op = OptionParser()
    op.add_option("-d", "--date",
                  action="store", dest="sel_date", default=None,
                  help="Date de sélection")
    (opts, args) = op.parse_args()
    if  opts.sel_date!=None:
        write_impact(opts.sel_date)

