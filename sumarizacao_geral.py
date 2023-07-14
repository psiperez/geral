import re
import nltk
import string
import heapq
from html.parser import HTMLParser
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from string import punctuation
from nltk.probability import FreqDist

#https://www.dn.pt/sociedade/ministra-quer-mais-mulheres-nas-forcas-armadas-mas-avisa-que-foco-nos-numeros-e-insuficiente-16554146.html#media-1


texto_original = '''
A ministra da Defesa Nacional realçou esta segunda-feira a importância estratégica do recrutamento de mais mulheres para as Forças Armadas mas avisou que o foco nos números é insuficiente, salientando a necessidade de integração na cultura militar.
O recrutamento de mulheres é estrategicamente importante no que diz respeito ao aumento da capacidade militar necessária para gerir os compromissos em matéria de defesa e segurança. Por isso, se precisamos de recrutar mais mulheres, precisamos que elas se sintam mais acolhidas, aceites e que pertencem, defendeu Helena Carreiras.
A governante falava na abertura do 5.º 'Erasmus Gender Seminar', um seminário dedicado ao tema "Perspetivas de Género no Ensino Superior", que se realiza esta segunda e terça-feira na Academia Militar, no concelho da Amadora, em Lisboa.
Numa intervenção em inglês, a ministra da Defesa alertou, no entanto, para uma excessiva concentração "nos números".
"A fórmula básica 'adicionar mulheres e agitar' simplesmente não é suficiente para desafiar a desigualdade estrutural e promover mudanças reais", salientou.
A este respeito, considerou Helena Carreiras, "é importante investigar em que medida os jovens cadetes, homens e mulheres, se adaptam (ou não) à cultura militar e ao seu ambiente predominantemente masculino, qual é o nível de aceitação pelos pares entre os cadetes e o que acontece quando as mulheres assumem cargos de liderança".
Salientando que "guerra e género sempre estiveram interligados", Helena Carreiras afirmou que "a cultura criou diferentes papéis de género, e a guerra, apesar de um número crescente de mulheres nas Forças Armadas, ainda é vista como uma atividade masculina, onde a maioria dos soldados ainda são homens".
"Isto justifica a questão de saber se a educação e a formação nas instituições de Estudos Superiores Militares continuam a privilegiar a criação de um soldado masculino", apontou a ministra, que é especialista em sociologia militar, com obra publicada sobre mulheres nas Forças Armadas.
De acordo com Helena Carreiras, "por um lado, a investigação demonstrou efeitos consistentes de masculinidade nas organizações militares, que se manifesta pelas percentagens assimétricas de pessoal masculino 'versus' feminino".
"Por outro lado, o treino militar básico é frequentemente descrito como um processo em que os militares doutrinam normas de masculinidade que tanto enaltecem as características masculinas, quanto diminuem a feminilidade", salientou.
Tendo em conta o atual "complexo cenário internacional", com novos desafios à segurança colocados pela crescente competição geopolítica, pelos avanços na tecnologia de guerra e ameaças híbridas, e pelas ameaças representadas pelas mudanças climáticas, sustentou Helena Carreiras, "a preparação dos nossos militares deve combinar cada vez mais treino para guerra simétrica e assimétrica, bem como treino para a construção da paz".
"Neste contexto, os soldados precisam de fazer mais do que apenas usar a força em nome do Estado. Precisam também de criar confiança, trabalhando lado a lado com sociedades e parceiros de contextos organizacionais distintos. Devem ser capazes de atacar as causas de fundo da guerra e criar condições mais favoráveis para uma paz a longo prazo", acrescentou.
Por isso, "combinar bravura e força com empatia e paciência -- duas características muitas vezes feminizadas -- pode, de facto, ser um multiplicador de força para o bem", destacou Helena Carreiras.
Numa intervenção momentos antes, o Chefe do Estado-Maior do Exército (CEME), general Eduardo Mendes Ferrão, adiantou que atualmente o ramo tem 1.293 mulheres, o que corresponde aproximadamente a 13% do total do pessoal.
"A igualdade é hoje um tema incontornável e a diversidade enriquece qualquer instituição. Por isso, é necessário desenvolver ações concretas que nos permitam olhar para o futuro e confiar que estamos a ir na direção de uma sociedade mais progressista", defendeu o general.


'''
#retira espaços no fim da frase
texto_original_mod = re.sub(r'\s+',' ',texto_original)
print (texto_original_mod)
#print (string.punctuation)


#cria função de pre-processamento
def pre_proc (x):
#retira as maiúsculas
    texto = x.lower()

#tokeniza
    tokens = [ ] 
    for i1 in word_tokenize (texto):
        tokens.append(i1)

        #retirar as stopwords dos tokens
        stopwords = nltk.corpus.stopwords.words("portuguese")
        tokens = [palavra for palavra in tokens if palavra not in stopwords
                  and palavra not in string.punctuation]

        #usa str em um laço for e concatena os elementos da lista com join
        #para voltar para forma de texto
        texto = ' '.join([str(i2) for i2 in tokens])
    #return tokens
    return texto

#aplica a função pre_proc
texto_formatado = pre_proc(texto_original)
print (texto_formatado)

#calcula a frequencia de distribuição das palavras do texto
frequencia_palavras = FreqDist(word_tokenize(texto_formatado))
print (dict(frequencia_palavras))

#cálculo da frequencia proporcional (peso das palavras)
frequencia_maxima = max(frequencia_palavras.values())

for i3 in frequencia_palavras.keys():
    frequencia_palavras[i3] = frequencia_palavras[i3]/frequencia_maxima

print(dict(frequencia_palavras))

#tokeniza por sentencas
#quebra frase em sentenças com ferramenta nltk específica
texto_sentenca = nltk.sent_tokenize(texto_original)
#print (list(texto_sentenca))

nota_sentencas = {}
#busca por todas as sentencas
for sentenca in texto_sentenca : 
    #print (sentencas)

    #busca por todas as palavras dentro das sentencas
    for palavra in nltk.word_tokenize(sentenca.lower()):
        #print (palavra)

        #condição if para calcular somatório dos valores das palavras
        #para o total da sentença
        
        if palavra in frequencia_palavras.keys():
            if sentenca not in nota_sentencas.keys():
                nota_sentencas[sentenca] = frequencia_palavras[palavra]
            else:
                nota_sentencas[sentenca] += frequencia_palavras[palavra]

print(dict(nota_sentencas))

#ordenação das sentenças a partir dos maiores valores
melhores_sentencas = heapq.nlargest(3,nota_sentencas,key = nota_sentencas.get)
print(melhores_sentencas)

#fazer o resumo a partir da ordenação
resumo = ' '.join(melhores_sentencas)
print(resumo)
