#!/usr/bin/python
#
# The Initial Developer of the Original Code is
# Sorcerer <sorcerer@gaglers.com>
#
import requests, time, sys

def get_list_ids(list_args, log_file):
    to_delete = []
    start = end = 0
    for arg in list_args:
        split_arr = arg.split(':')
        split_len = len(split_arr)
        if split_len == 2:
            try:
                start = int(split_arr[0])
                end = int(split_arr[1]) + 1
                for i in range(start, end):
                    to_delete.append(i)
            except:
                log_file.write("Invalid Range given: '%s'\n" % arg)
        elif split_len == 1:
            try:
                list_id = int(arg)
                to_delete.append(arg)
            except:
                log_file.write("Invalid list ID: '%s' not a number\n" % arg)
        log_file.flush()
    return to_delete

def main(argv):
    if len(argv) < 4:
        print "Usage: %s <slug> <access_token> <list_id> <list_id>" % argv[0]
        print "OR" 
        print "Usage: %s <slug> <access_token> <start:end>" % argv[0]
        return

    output = open('/tmp/listdelete.log', 'a')
    SLUG = argv[1]
    ACCESS_TOKEN= argv[2]
    to_delete = get_list_ids(argv[3:], output)
    log_text = ''
    for i in to_delete:
        try:
            url = "https://%s.nationbuilder.com/api/v1/lists/%s?access_token=%s" % \
                (SLUG, i, ACCESS_TOKEN)
            r = requests.delete(url)
            if r.status_code == 204:
                log_text = "Deleted list: %s at %s.nationbuilder.com\n" % (i, SLUG)
            elif r.status_code == 404:
                log_text = "No list: %s at %s.nationbuilder.com\n" % (i, SLUG)
            else:
                log_text = "Deletion Failed for list: %s at %s.nationbuilder.com,"\
                    " error code:%s. Try again later.\n" % (i, SLUG, r.status_code)
        except Exception as e:
            log_text = "Exceptions for url:%s Error:%s\n" % (url, str(e))
            pass
        output.write(log_text)
        output.flush()
        time.sleep(1)
    log_text = "\n\n"
    output.write(log_text)
    output.close()

if __name__ == "__main__":
    main(sys.argv)
