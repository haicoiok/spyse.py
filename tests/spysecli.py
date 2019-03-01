#!/usr/bin/python3

from pprint import pprint
from spyse import spyse
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-target', help="target")
parser.add_argument('-param', help="parameter to use (ip, domain, cidr, url, hash)")
parser.add_argument('-page', help="page")
parser.add_argument('--raw', help="show raw json", action="store_true")
parser.add_argument('--dns-ptr', help="show dns ptr records", action="store_true")
parser.add_argument('--dns-soa', help="show dns soa records", action="store_true")
parser.add_argument('--dns-mx', help="show dns mx records", action="store_true")
parser.add_argument('--dns-aaaa', help="show dns aaaa records", action="store_true")
parser.add_argument('--dns-ns', help="show dns ns records", action="store_true")
parser.add_argument('--dns-a', help="show dns a records", action="store_true")
parser.add_argument('--dns-txt', help="show dns txt records", action="store_true")
parser.add_argument('--dns-all', help="show all dns records", action="store_true")
parser.add_argument('--domains-with-same-ns', help="show domains with same ns", action="store_true")
parser.add_argument('--domains-using-as-mx', help="show domains using as mx", action="store_true")
parser.add_argument('--domains-on-ip', help="show domains on ip", action="store_true")
parser.add_argument('--subdomains-aggregate', help="show subdomains aggregate", action="store_true")
args = parser.parse_args()

s = spyse()

def get_dns_ptr(target, param, page, raw=False):
	if(raw == True):
		return(s.dns_ptr(target, param=param, page=page))
	else:
		data = s.dns_ptr(target, param=param, page=page)
		retval = ""

		for record in data['records']:
			retval += "PTR RECORD @ {} FROM HOSTNAME {}\n".format(
				record['ip']['ip'],
				record['hostname']
			)
		return retval
	return False

def get_dns_soa(target, param, page, raw=False):
	if args.raw:
		return print(s.dns_soa(target, param=param, page=page))
	else:
		data = s.dns_soa(target, param=param, page=page)
		retval = ""
		for record in data['records']:
			retval += "SOA RECORD @ {} FROM {} WITH SERIAL {}\n".format(
				record['domain']['domain'],
				record['domain']['ip']['ip'],
				record['serial']
			)
		return retval
	return False

def get_dns_mx(target, param, page, raw=False):
	if args.raw:
		return(s.dns_mx(target, param=param, page=page))
	else:
		data = s.dns_mx(target, param=param, page=page)
		retval = ""
		for record in data['records']:
			retval += "MX RECORD @ {} FROM IP {}\n".format(
				record['mx_domain']['domain'],
				record['mx_domain']['ip']['ip']
			)
		return retval
	return False

def get_dns_aaaa(target, param, page, raw=False):
	if args.raw:
		return s.dns_aaaa(target, param=param, page=page)
	else:
		data = s.dns_aaaa(target, param=param, page=page)
		retval = ""
		for record in data['records']:
			retval += "AAAA RECORD @ {} FROM IP {}\n".format(
				record['domain']['domain'],
				record['ipv6']
			)
		return retval
	return False

def get_dns_ns(target, param, page, raw=False):
	if args.raw:
		return s.dns_ns(target, param=param, page=page)
	else:
		data = s.dns_ns(target, param=param, page=page)
		retval = ""
		for record in data['records']:
			retval += "NS RECORD @ {} FROM {}\n".format(
				record['ns_domain']['domain'],
				record['ns_domain']['ip']['ip']
			)
		return retval
	return False

def get_dns_a(target, param, page, raw=False):
	if args.raw:
		print(s.dns_a(target, param=param, page=page))
		sys.exit()
	else:
		data = s.dns_a(target, param=param, page=page)
		retval = ""
		for record in data['records']:
			retval += "A RECORD @ {} FROM {}\n".format(
				record['domain']['domain'],
				record['ip']['ip']
			)
		return retval
	return False

def get_dns_txt(target, param, page, raw=False):
	if args.raw:
		return s.dns_txt(target, param=param, page=page)
	else:
		data = s.dns_txt(target, param=param, page=page)
		retval = "TXT RECORDS FROM {}\n".format(target)
		for record in data['records']:
			retval += '> {}\n'.format(record['data'])
		return retval
	return False


def get_domains_with_same_ns(target, param, page, raw=False):
	return s.domains_with_same_ns(target, param, page)


def get_domains_using_as_mx(target, param, page, raw=False):
	if args.raw:
		return s.domains_using_as_mx(target, param=param, page=page)
	else:
		data = s.domains_using_as_mx(target, param=param, page=page)
		retval = ""
		for record in data['records']:
			retval += "{} USING SAME MX AS {} ON IP {}\n".format(
				record['domain'],
				args.target,
				record['ip']['ip']
			)
		return retval
	return False

def get_domains_on_ip(target, param, page, raw=False):
	if args.raw:
		return s.domains_on_ip(target, param=param, page=page)
	else:
		retval = ""
		data = s.domains_on_ip(target, param=param, page=page)
		for record in data['records']:
			retval += "{}\n".format(record['domain'])
		return retval
	return False

def get_subdomains_aggregate(target, param, page, raw=False):
	if args.raw:
		return s.subdomains_aggregate(target, param=param, page=page)
	else:
		retval = ""
		data = s.subdomains_aggregate(target, param=param, page=page)['cidr']
		keys = data.keys()

		for key in keys:
			domains = data[key]['results']
			for d in domains:
				domain = d['data']['domains']
				if len(domain) > 1:
					for i in domain:
						retval += "{}\n".format(i)
				else:
					retval += "{}\n".format(domain[0])
		return retval
	return False

def get_dns_all(target, param, page, raw=False):
	data = ""
	if args.raw:
		data += get_dns_ptr(target, param=param, page=page, raw=True)
		data += get_dns_soa(target, param=param, page=page, raw=True)
		data += get_dns_mx(target, param=param, page=page, raw=True)
		data += get_dns_aaaa(target, param=param, page=page, raw=True)
		data += get_dns_a(target, param=param, page=page, raw=True)
		data += get_dns_ns(target, param=param, page=page, raw=True)
		data += get_dns_txt(target, param=param, page=page, raw=True)
	else:
		data += get_dns_ptr(target, param=param, page=page)
		data += get_dns_soa(target, param=param, page=page)
		data += get_dns_mx(target, param=param, page=page)
		data += get_dns_aaaa(target, param=param, page=page)
		data += get_dns_a(target, param=param, page=page)
		data += get_dns_ns(target, param=param, page=page)
		data += get_dns_txt(target, param=param, page=page)
	return data

if args.target and args.param:
	if args.page:
		page = args.page
	else:
		page = 1

	target = args.target
	param = args.param

	if args.dns_ptr:
		print(get_dns_ptr(args.target, args.param, page, raw=args.raw))

	if args.dns_soa:
		print(get_dns_soa(args.target, args.param, page, raw=args.raw))

	if args.dns_mx:
		print(get_dns_mx(args.target, args.param, page, raw=args.raw))

	if args.dns_aaaa:
		print(get_dns_aaaa(args.target, args.param, page, raw=args.raw))

	if args.dns_ns:
		print(get_dns_ns(args.target, args.param, page, raw=args.raw))

	if args.dns_a:
		print(get_dns_a(args.target, args.param, page, raw=args.raw))

	if args.dns_txt:
		print(get_dns_txt(args.target, args.param, page, raw=args.raw))

	if args.domains_with_same_ns:
		print(get_domains_with_same_ns(args.target, args.param, page, raw=args.raw))

	if args.domains_using_as_mx:
		print(get_domains_using_as_mx(args.target, args.param, page, raw=args.raw))

	if args.domains_on_ip:
		print(get_domains_on_ip(args.target, args.param, page, raw=args.raw))

	if args.subdomains_aggregate:
		print(get_subdomains_aggregate(args.target, args.param, page, raw=args.raw))

	if args.dns_all:
		print(get_dns_all(args.target, args.param, page, raw=args.raw))
