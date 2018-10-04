import os
import shutil
from mutatorMath.ufo import build
from mutatorMath.ufo.document import DesignSpaceDocumentReader, DesignSpaceDocumentWriter

currentFolder = os.getcwd()
mutatorSansFolder = os.path.join(os.path.dirname(currentFolder), 'MutatorSans')

designSpacePath = os.path.join(currentFolder,'MutatorSans_RulesDiagram.designspace')
ufosFolder = os.path.join(currentFolder, 'ufos')

outputFolder = '/_code/robofont_com/images/how-tos'
articleName = 'creating-glyph-substitution-rules'

master1 = 'LightCondensed'
master2 = 'LightWide'

f1 = OpenFont(os.path.join(mutatorSansFolder, 'MutatorSans%s.ufo' % master1), showInterface=False)
f2 = OpenFont(os.path.join(mutatorSansFolder, 'MutatorSans%s.ufo' % master2), showInterface=False)

c1 = 0, 0.7, 1
c2 = 0.8,
c3 = 1, 0, 0.4
c4 = 1, 0.7, 0

captionSize = 18

rule = 0.3

def clearInstances():
    for f in os.listdir(ufosFolder):
        if 'MutatorInterpolation_' in f:
            shutil.rmtree(os.path.join(ufosFolder, f))

def makeInstances(stepsWeight, stepsWidth):
    doc = DesignSpaceDocumentWriter(designSpacePath, verbose=True)

    doc.addSource(
        os.path.join(mutatorSansFolder, "MutatorSansLightCondensed.ufo"),
        name="LightCondensed",
        location=dict(weight=0, width=0),
        copyInfo=True,
        familyName="MutatorSans",
        styleName="LightCondensed")

    doc.addSource(
        os.path.join(mutatorSansFolder, "MutatorSansLightWide.ufo"),
        name="LightWide",
        location=dict(weight=0, width=1))

    doc.addSource(
        os.path.join(mutatorSansFolder, "MutatorSansBoldCondensed.ufo"),
        name="BoldCondensed",
        location=dict(weight=1, width=0))

    doc.addSource(
        os.path.join(mutatorSansFolder, "MutatorSansBoldWide.ufo"),
        name="BoldWide",
        location=dict(weight=1, width=1))

    for i in range(stepsWeight):
        wt = i * 1.0 / (stepsWeight-1)
        for j in range(stepsWidth):
            wd = j * 1.0 / (stepsWidth-1)
            doc.startInstance(
                fileName=os.path.join(ufosFolder, "MutatorSansInstance_%s-%s.ufo" % (int(wt*1000), int(wd*1000))),
                familyName="MutatorSansExample",
                styleName="%s-%s" % (int(wt*1000), int(wd*1000)),
                location=dict(weight=wt, width=wd))
            doc.endInstance()

    doc.save()

    doc = DesignSpaceDocumentReader(designSpacePath, 3, roundGeometry=True, verbose=False)
    doc.process(makeGlyphs=True, makeKerning=False, makeInfo=False)

def drawTracks(saveImg=False):

    steps = 11
    shiftX = 50
    shiftY = 120
    pageWidth, pageHeight = 1000, 260

    y1 = shiftY
    x1 = 200
    x2 = 900

    s = 0.13
    sw = 5
    r = 6

    newPage(pageWidth, pageHeight)
    translate(60, 80)

    save()

    strokeWidth(sw)
    lineCap('round')
    fill(None)

    # lines gray
    stroke(*c2)
    strokeWidth(4)
    lineDash(2, 7)
    line((x1, 0), (x2, 0))
    line((0, y1), (x1, y1))

    # lines blue
    newPath()
    stroke(*c1)
    line((x1, 0), (x1, y1))
    lineDash(None)
    line((x1, y1), (x2, y1))
    line((0, 0), (x1, 0))

    # circles
    strokeWidth(4)
    stroke(*c1)
    fill(1)
    oval(x1-r, -r, r*2, r*2)
    oval(x1-r, y1-r, r*2, r*2)

    # glyph name captions
    with savedState():
        fill(*c3)
        font('RoboType-Mono')
        stroke(None)
        fontSize(captionSize)

        for glyphName in ['I.narrow', 'I']:
            save()
            fill(*c3)
            font('RoboType-Mono')
            fontSize(captionSize)
            rotate(90)
            text(glyphName, (0, 30))
            restore()
            translate(0, shiftY)

    # values captions
    with savedState():
        fill(*c3)
        font('RoboType-Mono')
        stroke(None)
        fontSize(captionSize)

        w = shiftX
        for i in range(steps):
            factor = i * 1.0 / (steps-1)
            text(str(int(factor*1000)), (5, -40))
            translate(w, 0)
            w *= 1.1

    restore()

    if saveImg:
        imgPath = os.path.join(outputFolder, '%s_tracks.png' % articleName)
        saveImage(imgPath)

def drawTracksGlyph(saveImg=False):

    pageWidth, pageHeight = 1000, 340

    steps = 11
    shiftX = 50
    shiftY = 120
    s = 0.13

    newPage(pageWidth, pageHeight)
    translate(60, 80)

    glyphMasters = [
        (f1['I.narrow'], f2['I.narrow']),
        (f1['I'], f2['I']),
    ]

    for n, (g1, g2) in enumerate(glyphMasters):

        save()
        w = shiftX
        for i in range(steps):
            factor = i * 1.0 / (steps-1)
            g = RGlyph()
            g.interpolate(factor, g1, g2)

            if n == 0:
                color1, color2 = c1, c2
            else:
                color2, color1 = c1, c2

            if factor <= 0.3:
                fill(*color1)
            else:
                fill(*color2)

            save()
            scale(s)
            drawGlyph(g)
            restore()

            if n == 0:
                with savedState():
                    fill(*c3)
                    font('RoboType-Mono')
                    fontSize(captionSize)
                    text(str(int(factor*1000)), (5, -40))

            translate(w, 0)
            w *= 1.1

        restore()

        # draw caption
        save()
        fill(*c3)
        font('RoboType-Mono')
        fontSize(captionSize)
        rotate(90)
        text(g1.name, (0, 30))
        restore()

        translate(0, shiftY)

    if saveImg:
        imgPath = os.path.join(outputFolder, '%s_tracks-glyph.png' % articleName)
        saveImage(imgPath)

def drawSubstitutionAxis(saveImg=False):

    steps  = 11
    shiftX = 50
    shiftY = 120

    s = 0.13

    pageWidth, pageHeight = 1000, 230

    newPage(pageWidth, pageHeight)
    translate(30, 80)

    with savedState():
        w = shiftX
        for i in range(steps):
            factor = i * 1.0 / (steps-1)
            g = RGlyph()

            if factor <= 0.3:
                glyphName = 'I.narrow'
            else:
                glyphName = 'I'

            g1 = f1[glyphName]
            g2 = f2[glyphName]
            g.interpolate(factor, g1, g2)

            save()
            scale(s)
            fill(*c1)
            drawGlyph(g)
            restore()

            translate(w, 0)
            w *= 1.1

    # values captions
    with savedState():
        fill(*c3)
        font('RoboType-Mono')
        stroke(None)
        fontSize(captionSize)

        w = shiftX
        for i in range(steps):
            factor = i * 1.0 / (steps-1)
            text(str(int(factor*1000)), (5, -40))
            translate(w, 0)
            w *= 1.1

    if saveImg:
        imgPath = os.path.join(outputFolder, '%s_substitution-axis.png' % articleName)
        saveImage(imgPath)

def drawSubstitutionDesignspace(mode=1, saveImg=False):

    # mode 0 : partial diagrams
    # mode 1 : combined diagram

    pageWidth, pageHeight = 1000, 650

    stepsWeight = 6
    stepsWidth  = 11
    shiftX = 50
    shiftY = 90
    s = 0.085

    glyphNames = ['I', 'I.narrow']

    # clearInstances()
    # makeInstances(stepsWeight, stepsWidth)

    if mode == 0:

        for n, glyphName in enumerate(glyphNames):

            newPage(pageWidth, pageHeight)
            translate(60, 80)

            for i in range(stepsWeight):
                wt = i * 1.0 / (stepsWeight-1)

                save()

                w = shiftX
                for j in range(stepsWidth):
                    wd = j * 1.0 / (stepsWidth-1)

                    fileName = 'MutatorSansInstance_%s-%s.ufo' % (int(wt*1000), int(wd*1000))
                    ufoPath  = os.path.join(ufosFolder, fileName)
                    f = OpenFont(ufoPath, showInterface=False)
                    g = f[glyphName]

                    save()
                    scale(s)

                    if glyphName == 'I':
                        if wd <= 0.3:
                            fill(*c2)
                        else:
                            fill(*c1)
                    else:
                        if wd <= 0.3:
                            fill(*c1)
                        else:
                            fill(*c2)

                    drawGlyph(g)
                    restore()

                    if i == 0:
                        with savedState():
                            fill(*c3)
                            font('RoboType-Mono')
                            fontSize(captionSize)
                            text(str(j*100), (5, -40))

                    translate(w, 0)
                    w *= 1.1

                restore()

                # draw caption
                save()
                fill(*c3)
                font('RoboType-Mono')
                fontSize(captionSize)
                rotate(90)
                text(str(i*100*2), (0, 30))
                restore()

                translate(0, shiftY)

            if saveImg:
                imgPath = os.path.join(outputFolder, '%s_substitution-designspace-partial-%s.png' % (articleName, n+1))
                saveImage(imgPath)

    else:

        newPage(pageWidth, pageHeight)
        translate(60, 80)

        for i in range(stepsWeight):
            wt = i * 1.0 / (stepsWeight-1)
            save()
            w = shiftX
            for j in range(stepsWidth):
                wd = j * 1.0 / (stepsWidth-1)

                fileName = 'MutatorSansInstance_%s-%s.ufo' % (int(wt*1000), int(wd*1000))
                ufoPath  = os.path.join(ufosFolder, fileName)
                f = OpenFont(ufoPath, showInterface=False)

                if wd <= 0.3:
                    g = f['I.narrow']
                else:
                    g = f['I']

                save()
                fill(*c1)
                scale(s)
                drawGlyph(g)
                restore()

                if i == 0:
                    with savedState():
                        fill(*c3)
                        font('RoboType-Mono')
                        fontSize(captionSize)
                        text(str(j*100), (5, -40))

                translate(w, 0)
                w *= 1.1

            restore()

            # draw caption
            save()
            fill(*c3)
            font('RoboType-Mono')
            fontSize(captionSize)
            rotate(90)
            text(str(i*100*2), (0, 30))
            restore()

            translate(0, shiftY)

        if saveImg:
            imgPath = os.path.join(outputFolder, '%s_substitution-designspace.png' % articleName)
            saveImage(imgPath)

#-------------
# make images
#-------------

saveImgs = False

# drawTracks(saveImgs)
# drawTracksGlyph(saveImgs)
# drawSubstitutionAxis(saveImgs)
drawSubstitutionDesignspace(1, saveImgs)
