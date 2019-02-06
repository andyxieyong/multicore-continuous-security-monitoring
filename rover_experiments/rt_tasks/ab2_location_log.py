# import geocoder

# reads values and log to /roverlog/loctionlog.txt


if __name__ == '__main__':

    # g = geocoder.ip('me')
    # geoval = str(g.latlng)
    # print "latlang", g.latlng
    # static for now
    geoval = "[39.1097, -84.5046]"

    filename = '../roverlog/locationlog.txt'

    with open(filename, "a") as f:
        f.write(geoval + '\n')
