import libtorrent as lt



torinfo = lt.torrent_info('torrent/test.torrent')
name = torinfo.name()
file_list = torinfo.files()
num_files = torinfo.num_files()
total_size = torinfo.total_size()
#result, name = check_format(name, file_list)

print name, 
#print file_list
for i in file_list:
    print i.path
    print i.size
    #print dir(i)
print num_files
print total_size
 
