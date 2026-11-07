#!/usr/bin/env python3
"""Gera o banco de dados FICTÍCIO usado na apresentação (data/mock-db.js e data/mock-db.json).
Nenhum dado aqui é de pessoa ou venda real. Rode: python3 scripts/gerar_mock.py"""
import json, random, pathlib
random.seed(2026)
OUT = pathlib.Path(__file__).resolve().parent.parent / "data"
uid = lambda p, i: f"{p}{i:04d}"

nomes = [("Marina Alves","1990-11-14"),("Carlos Eduardo Souza","1985-03-02"),("Juliana Prado","1993-11-27"),("Rafaela Mendes","1988-07-19"),
 ("Thiago Ribeiro","1991-01-30"),("Patrícia Lima","1979-09-08"),("Fernanda Castro","1995-05-21"),("Bruno Teixeira","1987-12-05"),
 ("Camila Duarte","1992-02-11"),("Lucas Fernandes","1996-08-16"),("Aline Moreira","1983-04-25"),("Diego Barros","1990-10-09"),
 ("Beatriz Nogueira","1998-06-03"),("Renata Campos","1981-03-18")]
clientes = []
for i,(n,nasc) in enumerate(nomes, 1):
    clientes.append({"id":uid("c",i),"nome":n,
      "cpf":f"000.000.000-{10+i:02d}" if i%3==0 else "",
      "endereco":f"Rua Exemplo, {100+i*7} - São Paulo/SP" if i%2==0 else "",
      "email":n.lower().replace(" ","."). replace("é","e").replace("í","i").replace("ú","u").replace("ã","a")+"@exemplo.com.br" if i%4!=0 else "",
      "telefone":f"119000000{i:02d}","nascimento":nasc,
      "consentimento":f"2026-0{random.randint(1,9)}-{random.randint(10,28)}","criado":"2026-01-10"})

fem = [43,43,43,43,49,41,21,31,11,28,51,40,54,35,45,16,13,9,2,38]
mas = [49,49,23,23,21,30,14,15,16,20,35,6]
extras = ["Baunilha e âmbar","Lavanda e cedro","Fougère amadeirado","Flor de laranjeira","Chá branco e musk","Oud suave"]
pags = ["PIX"]*5+["Crédito"]*3+["Débito"]*2+["Dinheiro","Pagamento online"]
vendas = []
def add(data, desc, cli, produto, frag, extra, qtd, pag, valor):
    vendas.append({"id":uid("v",len(vendas)+1),"data":data,"desc":desc,"cliente":cli,"tipo":"Receita","cat":"Receita Operacional Bruta",
      "produto":produto,"frag":frag,"extra":extra,"qtd":qtd,"pag":pag,"valor":valor})
ativos = [c["id"] for c in clientes[:9]]   # compram até novembro
inativos = [c["id"] for c in clientes[9:]]  # última compra em julho/agosto (aparecem em "sem comprar há 60+ dias")
for _ in range(80):
    m = random.randint(1,10); d = random.randint(1,28)
    data = f"2026-{m:02d}-{d:02d}"
    cli = random.choice(ativos+[""]*3) if m>8 else random.choice(ativos+inativos+[""]*3)
    if cli in inativos and m>8: cli = random.choice(ativos)
    r = random.random()
    if r<0.45:
        n = random.choice(fem); q=1; p="Perfume 50ml" if random.random()<.6 else "Perfume 15ml"; v=(120 if p=="Perfume 50ml" else 45)*q
        add(data,f"IF {n:02d}",cli,p,f"IF{n:02d}","",q,random.choice(pags),v)
    elif r<0.70:
        n = random.choice(mas); p="Perfume 50ml" if random.random()<.6 else "Perfume 15ml"; v=120 if p=="Perfume 50ml" else 45
        add(data,f"IM {n:02d}",cli,p,f"IM{n:02d}","",1,random.choice(pags),v)
    elif r<0.80:
        add(data,"Pedido sob demanda",cli,"Perfume 50ml","EXTRA",random.choice(extras),1,random.choice(pags),150)
    elif r<0.90:
        add(data,"Água de lençol",cli,"Água de lençol 200ml","","",random.randint(1,2),random.choice(pags),55)
    else:
        add(data,"Vela aromática",cli,"Velas aromáticas","","",random.randint(1,3),random.choice(pags),28)
# garante inativos com última compra antiga
for i,cid in enumerate(inativos):
    add(f"2026-0{7+i%2}-{10+i:02d}",f"IF {fem[i]:02d}",cid,"Perfume 15ml",f"IF{fem[i]:02d}","",1,"PIX",45)
vendas.sort(key=lambda x:x["data"])
for i,v in enumerate(vendas,1): v["id"]=uid("v",i)

cat = {"Insumos e Matérias-primas":["Essência para perfume","Álcool de cereais","Frascos de vidro"],
       "Logística":["Uber para a loja","Taxa de entrega"],"Fixas e Operacionais":["Aluguel da loja","Internet","Celular da loja"],
       "Impostos Extras":["Taxa de manutenção"]}
tipo = {"Insumos e Matérias-primas":"Custo Variável","Logística":"Custo Variável","Fixas e Operacionais":"Despesas Adm","Impostos Extras":"Impostos"}
custos=[]
for m in range(1,11):
    for c in random.sample(list(cat),3):
        custos.append({"id":"","data":f"2026-{m:02d}-{random.randint(1,28):02d}","desc":random.choice(cat[c]),"tipo":tipo[c],"cat":c,
                       "pag":random.choice(["PIX","Crédito","Débito"]),"valor":round(random.uniform(30,420),2)})
custos.sort(key=lambda x:x["data"])
for i,c in enumerate(custos,1): c["id"]=uid("g",i)

produtos=[("Perfume 50ml","Perfume",120,38),("Perfume 15ml","Perfume",45,14),("Perfume extra (sob demanda)","Perfume extras",150,50),
          ("Água de lençol 200ml","Água de lençol",55,18),("Velas aromáticas","Vela",28,9)]
prods=[{"id":uid("p",i),"nome":n,"cat":c,"preco":p,"custo":k} for i,(n,c,p,k) in enumerate(produtos,1)]

# histórico fictício (números inventados, só para o painel não abrir vazio)
rec=[round(random.uniform(3500,9500)) for _ in range(10)]+[0,0]
desp=[round(r*random.uniform(.45,.8)) for r in rec]
tot=sum(rec)
hist={"rec":rec,"desp":desp,
 "prod":{"Perfume 50ml":round(tot*.55),"Perfume 15ml":round(tot*.2),"Água de lençol 200ml":round(tot*.1),"Velas aromáticas":round(tot*.05),"Vidros variáveis":round(tot*.1)},
 "pag":{"PIX":round(tot*.42),"Crédito":round(tot*.3),"Débito":round(tot*.14),"Dinheiro":round(tot*.06),"Pagamento online":round(tot*.08)},
 "cat":{"Fixas e Operacionais":round(sum(desp)*.3),"Insumos e Matérias-primas":round(sum(desp)*.35),"Logística":round(sum(desp)*.1),"Demais categorias":round(sum(desp)*.25)},
 "frag":{"Feminino":round(tot*.65),"Masculino":round(tot*.25)}}
# DRE fictício por mês, coerente com rec/desp acima
shares={"PIX":.42,"Crédito":.3,"Débito":.14,"Dinheiro":.06,"Pagamento online":.08}
dre={"rb":{k:[round(r*v,2) for r in rec] for k,v in shares.items()},
     "ded":{"Desconto concedido":[round(r*.04,2) for r in rec]}}
rest=[d-round(r*.04,2) for d,r in zip(desp,rec)]
dre["cv"]={"Insumos e Matérias-primas":[round(x*.30,2) for x in rest],"Materiais de consumo":[round(x*.1,2) for x in rest],"Logística":[round(x*.05,2) for x in rest]}
dre["adm"]={"Fixas e Operacionais":[round(x*.35,2) for x in rest]}
dre["pes"]={"Sócios":[round(x*.2,2) for x in rest]}
dre["imp"]={}
hist["dre"]=dre
hf={}
for n in sorted(set(fem)|set(range(1,30,2))):
    q=random.randint(1,40) if n in fem[:6] else random.randint(1,8); hf[f"IF{n:02d}"]=[q,q*random.choice([45,85,120])]
for n in sorted(set(mas)|{1,5,9,22}):
    q=random.randint(1,18); hf[f"IM{n:02d}"]=[q,q*random.choice([45,85,120])]

db={"_aviso":"DADOS FICTÍCIOS. Gerado por scripts/gerar_mock.py. Não contém pessoas nem vendas reais.",
    "clientes":clientes,"vendas":vendas,"custos":custos,"produtos":prods,"historico":hist,"hf":hf}
(OUT/"mock-db.json").write_text(json.dumps(db,ensure_ascii=False,indent=1),encoding="utf-8")
(OUT/"mock-db.js").write_text("/* DADOS FICTÍCIOS para a apresentação. Gerado por scripts/gerar_mock.py */\nwindow.MOCK_DB = "+json.dumps(db,ensure_ascii=False)+";\n",encoding="utf-8")
print(len(clientes),"clientes",len(vendas),"vendas",len(custos),"custos")
