
messages = (
    #east 1
    ('2010132233040411302321143130330040240005', '0320412200014222421222201100032013411135', '3102210440002001040401441420330220342415', '2313131300311321201422313314413414412115', '0140032121141300411101002412410040310015', '0403314323411221010100401204124424424025', '133312203301031131112112103223145', '13104242241303041102031232043135'),
    #west 1
    ('3110132233040411302321143130330040240045', '0320412200014222421222201100032013411015', '0202010440001040440401441420330220341315', '1112131300011020201422313314413414414015', '2122233032440002432311102212310310220435', '4034314012221113402103014133412213301325', '024142214222030242001232124023232014035', '31013221121302032222004223103132241135'),
    #east 2
    ('1210132233040411302321143130330040240045', '1320412200014222421222201100032013411325', '3020132300442101430012141403110241042235', '1024411132222314033301302310103224414225', '0141130301441020203111142410342321321125', '1411201200401030221224020400001032210405', '0011322100422310432420131030102003002215', '0201422403120313302310001033104412014225', '0342010431011002001245', '1314020220201413223115'),
    #west 2
    ('3010143042311111301032001142111420421445', '1320410024412002221410132400222201204025', '1101202100440120220141002021300132433125', '4011301120103223134314223132130311000035', '1431102230242242010212231422001031112235', '2034012300412222131322202302421402114405', '1222010000121431012333120102242032215', '0110101013212311030320302413203220305'),
    #east 3
    ('2210143040001003022202312222321441442115', '3320410022224313410032420000102200424315', '3132233121201340041413023100012310431305', '0200201400020212123111000031122201100325', '1402142220230420012142412112231040100345', '0030210313002122103100003123320032404225', '0012402410202320430430312241313123011425', '2323111302110210202223414121132403212305', '0010301242212240330032110242131332310015', '4102101033004320314121114223304034000415', '041240123045', '04230101045'),
    #west 3
    ('1110143040440231010332321201132400320235', '4320410023421203014412122224014202111305', '0330311342241441113030031422340421311125', '4314132002101412021124312302031114300215', '1031332142002300111430341430331101221205', '1011322111204423101313212310203110222005', '1201201231300110240141330210230022200445', '2103122200014401220032321421413321312205', '1202240222342030331202440402005', '0021211001411022421034024114425'),
    #east 4
    ('1010143040001000000102132331201421330035', '2320410022224312124304303001102034211305', '1010042232100343001442142240222003000225', '3034110223132024033020302224411420101415', '1432343001202422301103013020010400301305', '0123324013413413024413014124122223033225', '2122221431303020131021131022300031032325', '4323314110324032001221031124314401202315', '122024230101311232213035', '34212102201003230340345'),
    #west 4
    ('3010143040001000000102132331201400400025', '2320410022224312124304303001102221131425', '2113102140010321222411243001001312233135', '0302212301323014304134203000323324211405', '0402102401032022102430210121030120332325', '4022111031324121021424403111220214311415', '2042332412033020233010412042410122321015', '3111403114212321224102401324400302214405', '2243141140421211141401305', '0202310000310001021400115'),
    #east 5
    ('1110143040001000000102132331201430441335', '3320410022224312124304303001102111124305', '1012142233020240141442122222302122132335', '3034110224012020413020022424202403412025', '0141101141031110102401102040100131001305', '2112111301104412111124034101220400412135', '1020410412211341301330132430110420102215', '0202030022400101204423110421111420311025', '1312242202220415', '2324421013314315')
    )

#convert string to ints
messages = tuple(map(lambda a: tuple(map(lambda b: tuple(map(lambda c: int(c),b)), a)), messages))



tris = list()

c = [0]*5

def handleTri(tri):
    n = []
    
    for t in tri:
        c[t]+=1
        n.append((0,1,1,1,2)[t])
    tris.append(tuple(n))

for m in messages:
    for y in range(0,len(m),2):
        x=0
        while x < len(m[y])-1:
            t1 = (m[y][x], m[y][x+1], m[y+1][x])
            handleTri(t1)
            x += 2
            
            if x >= len(m[y])-1:
                break

            t2 = (m[y+1][x], m[y+1][x-1], m[y][x])
            handleTri(t2)
            x+=1


for i in range(5):
    print(i, c[i]/sum(c))
#individualTris = set(tris)
#for t in individualTris:
    #print(t, tris.count(t)/len(tris))
            
            
        
