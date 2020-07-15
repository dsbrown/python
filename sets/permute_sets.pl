
#given set (a,b),(a,c),(a,d) return: (b,a),(c,a),(d,a),(a,b),(a,c),(a,d)
def permute_combinaton(azpairs):
    p = []
    for a,b in azpairs:
        p += [(a,b),(b,a)]
    return p

# # given a and (b,c,d,e,f) return (a,b),(a,c),(a,d),(a,e),(a,f)
def combinaton_site_AZ(site,az):
    return [(site,x) for x in az]

