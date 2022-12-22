def distance(str1, str2):
  d=dict()
  for i in range(len(str1)+1):
     d[i]=dict()
     d[i][0]=i
  for i in range(len(str2)+1):
     d[0][i] = i
  for i in range(1, len(str1)+1):
     for j in range(1, len(str2)+1):
        d[i][j] = min(d[i][j-1]+1, d[i-1][j]+1, d[i-1][j-1]+(not str1[i-1] == str2[j-1]))
  return d[len(str1)][len(str2)]

def Sugestion(query, terms: dict[str, float], alpha=0.3):
   # sugerencia sintactica, no semantica, de palabras parecidas a las de la query
   sugestions: dict[str, str] = {}
   max_weights: dict[str, float] = dict(zip(query.split(' '), [0]*len(query)))
   for d_term in terms:
      for q_term, w_q_t in max_weights.items():
         if abs(len(d_term) - len(q_term)) > alpha*4: continue
         term_weight = 4 + (1-alpha)*terms[d_term] - alpha*distance(d_term, q_term)
         if w_q_t < term_weight:
            max_weights[q_term] = term_weight
            sugestions[q_term] = d_term
   return sugestions