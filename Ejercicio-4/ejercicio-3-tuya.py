from HTMLImageEncoder import HTMLImageEncoder


encoder = HTMLImageEncoder("../data/html_sources")
result = encoder.encode_html_imgs()
print(result)