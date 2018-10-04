'''
Generate illustrations used in the article “Creating variable fonts”:
http://robofont.com/documentation/how-tos/creating-variable-fonts/

'''
import os

mutatorSansFolder = os.path.join(os.path.dirname(os.getcwd()), 'MutatorSans')
mutatorSansTTFPath = os.path.join(mutatorSansFolder, 'MutatorSans.ttf')

outputFolder = '/_code/robofont_com/images/how-tos'
articleName = 'creating-variable-fonts'

x0, y0 = 110, 100
x1, y1 = 790, 390
dx, dy = 20, 20

c1 = 1, 0, 0.4
c2 = 0, 0.7, 1
c3 = 1, 0.7, 0

captionSize = 21

masters = [
    ((0, 0), 'Light Condensed'),
    ((1, 0), 'Bold Condensed'),
    ((0, 1), 'Light Wide'),
    ((1, 1), 'Bold Wide'),
]

instances = [
    ((0.5, 0.327), 'Medium'),
    # ((0.7, 0.7), 'Test'),
]

def drawLocation(xy, color, mode=0):
    x, y = xy
    r = 8
    if mode == 0:
        fill(1)
    else:
        fill(*color)
    stroke(*color)
    strokeWidth(5)
    lineDash(None)
    oval(x-r, y-r, r*2, r*2)

def drawCaption(fontName, fontParamaters, xy, mode=0):

    wt, wd = fontParamaters
    x, y = xy

    x += dx
    y += dy

    txt = fontName

    if mode == 1:
        txt += '\n(%s, %s)' % (int(wd*1000), int(wt*1000))
        y += dy * 1.4

    fill(0)
    stroke(None)
    text(txt, (x, y))

def drawAxes(mode=0):

    save()

    stroke(*c2)
    strokeWidth(4)
    lineCap('round')

    if mode == 0:
        lineDash(3, 7)
    line((x0, y0), (x1, y0))
    line((x0, y0), (x0, y1))

    if mode == 1:
        lineDash(3, 7)
    line((x0, y1), (x1, y1))
    line((x1, y0), (x1, y1))

    for (wt, wd), instance in instances:
        x = x0 + (x1 - x0) * wd
        y = y0 + (y1 - y0) * wt
        line((x, y0), (x, y1))
        line((x0, y), (x1, y))

    restore()

    D = 60
    h = captionSize * 1.2

    # stroke(0.7)
    # line((x0, y0-D), (x1, y0-D))
    # line((x0-D, y0), (x0-D, y1))

    font('RoboType-Mono')
    fontSize(captionSize)
    stroke(None)
    fill(*c2)
    textBox('width', (x0, y0-D-h*0.5, x1-x0, h), align='center')

    if mode == 1:
        textBox('0', (x0, y0-D-h*0.5, x1-x0, h), align='left')
        textBox('1000', (x0, y0-D-h*0.5, x1-x0, h), align='right')

    save()
    translate(x0-D+h*0.5, y0)
    rotate(90)

    # save()
    # fill(None)
    # stroke(1, 0, 0)
    # stroke(0.7)
    # rect(0, 0, y1-y0, h)
    # restore()

    textBox('weight', (0, 0, y1-y0, h), align='center')

    if mode:
        textBox('0', (0, 0, y1-y0, h), align='left')
        textBox('1000', (0, 0, y1-y0, h), align='right')

    restore()

def drawDesignspaceDiagram(saveImg=False, mode=0):

    # mode 0 : "sketch mode"
    # mode 1 : axes & locations

    newPage(1000, 500)
    fill(1)
    rect(0, 0, width(), height())

    drawAxes(mode=mode)

    font('RoboType-Mono')
    fontSize(captionSize)

    for (wt, wd), master in masters:
        x = [x0, x1][wd]
        y = [y0, y1][wt]
        drawLocation((x, y), color=c1)
        drawCaption(master, (wt, wd), (x, y), mode=mode)

    for (wt, wd), instance in instances:
        x = x0 + (x1 - x0) * wd
        y = y0 + (y1 - y0) * wt
        drawLocation((x, y), color=c3)
        drawCaption(instance, (wt, wd), (x, y), mode=mode)

    if saveImg:
        if mode == 0:
            imgName = '%s_MutatorSans-design-space.png' % articleName
        else:
            imgName = '%s_MutatorSans-design-space-2.png' % articleName
        imgPath = os.path.join(outputFolder, imgName)
        saveImage(imgPath)

def drawMastersPreview(saveImg=False):

    ptSize = 90

    newPage(1000, 500)
    translate(40, 380)
    stroke(0)
    fontSize(ptSize)

    for (wt, wd), master in masters:
        wt = wt * 1000 if wt > 0 else 1
        wd = wd * 1000 if wd > 0 else 1
        font(mutatorSansTTFPath)
        fontVariations(wght=wt, wdth=wd)
        txt = master.replace('MutatorSans', '')
        text(txt.upper(), (0, 0))
        translate(0, -ptSize * 1.2)

    if saveImg:
        imgPath = os.path.join(outputFolder, '%s_MutatorSans-masters.png' % articleName)
        saveImage(imgPath)

def drawMastersContours(saveImg=False):

    glyphName = 'R'

    weights = ['Light', 'Bold']
    widths  = ['Condensed', 'Wide']

    x, y = 20, 40
    w, h = 340, 230

    s = 0.27
    r = 12

    newPage(1000, 300)

    fill(None)
    stroke(0)
    strokeWidth(5)
    lineJoin('round')
    font('RoboType-Mono')
    fontSize(18)
    translate(x, y)
    scale(s)

    for i, wt in enumerate(weights):
        for j, wd in enumerate(widths):
            ufoPath = os.path.join(mutatorSansFolder, 'MutatorSans%s%s.ufo' % (wt, wd))
            f = OpenFont(ufoPath, showInterface=False)
            g = f[glyphName]
            drawGlyph(g)
            save()
            fill(0)
            stroke(None)
            for c in g.contours:
                for pt in c.bPoints:
                    ptx, pty = pt.anchor
                    oval(ptx-r, pty-r, r*2, r*2)
            restore()
            translate(g.width, 0)

    if saveImg:
        imgPath = os.path.join(outputFolder, '%s_MutatorSans-contours.png' % articleName)
        saveImage(imgPath)

#-------------
# make images
#-------------

saveImgs = False

drawDesignspaceDiagram(saveImgs)
drawDesignspaceDiagram(saveImgs, mode=1)
drawMastersPreview(saveImgs)
drawMastersContours(saveImgs)
