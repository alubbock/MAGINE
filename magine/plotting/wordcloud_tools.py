from magine.plotting.wordcloud_mod import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import magine.ontology.enrichment_tools as et

process_dbs = [
    'GO_Biological_Process_2017',
    'Humancyc_2016',
    'Reactome_2016',
    'KEGG_2016',
    'NCI-Nature_2016',
    'Panther_2016',
    'WikiPathways_2016',
]

pd.set_option('display.width', 10000)
pd.set_option('max_colwidth', 100)


def word_cloud_from_array(enrichment_array, category, sample_ids,
                          database_list=process_dbs, save_name=None):
    samples = []
    all_samples = []
    for i in sample_ids:
        sample = et.filter_dataframe(enrichment_array, p_value=0.05,
                                     db=database_list, category=category,
                                     sample_id=i)
        all_samples.append(sample)
        if len(sample) != 0:
            if save_name is not None:
                output = "{}_{}_wordcloud".format(save_name, i)
            else:
                output = None
            hits_1 = create_wordcloud(sample, save_name=output)
            df1 = pd.DataFrame(hits_1.items(), columns=['words', 'counts'])
            df1.sort_values('counts', ascending=False, inplace=True)
            df1['sample'] = i
            samples.append(df1.copy())

    df = pd.concat(samples)
    samples = df['sample'].unique()
    df = pd.pivot_table(df, index='words', columns=['sample']).fillna(0)
    df.columns = df.columns.droplevel()
    df['sum'] = df[samples].sum(axis=1)
    df.sort_values('sum', ascending=False, inplace=True)
    print("\nSorted by sum of all")
    print(df.sort_values('sum', ascending=False).head(25))
    return all_samples, df


basic_words = {'signaling', 'signalling', 'receptor', 'events', 'protein',
               'proteins', 'regulation', 'interactions', 'via', 'signal',
               'mediated', 'pathway', 'activity', 'complex', 'positive',
               'mrna', 'cellular', 'viral', 'host', 'processing', 'activation',
               'rrna', 'network', 'rna', 'cancer', 'disease', 'cascade',
               'transcript', 'influenza', 'beta', 'pathways', 'gene', 'hiv',
               'downstream', 'activated', 'target',
               }


# basic_words = set()


def cleanup_term_name(row):
    x = row['term_name'].split('_')[0].lower()
    x = ' ' + x
    x = x.replace(' p53', ' tp53')
    x = x.replace('  ', ' ')
    if x[0] == ' ':
        x = x[1:]
    if x[-1] == ' ':
        x = x[:-1]
    return x


def create_wordcloud(df, save_name=None):
    data = df.apply(cleanup_term_name, axis=1)
    text = ' '.join(data)
    # Generate a word cloud image
    wc = WordCloud(margin=0, background_color=None, mode='RGBA', min_count=1,
                   width=800, height=600, collocations=True,
                   stopwords=basic_words)
    wordcloud = wc.generate(text)
    word_dict = wc.process_text(text)
    # for i,j in sorted(word_dict.items(), key=lambda p:p[1], reverse=True):
    #     print("{} : {}".format(i, j))
    # Display the generated image:
    # the matplotlib way:
    if save_name is not None:
        plt.figure()
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.xticks([])
        plt.yticks([])
        plt.axis("off")
        plt.savefig('{}.png'.format(save_name), bbox_inches='tight', dpi=150)
        plt.title(save_name)
    plt.show()
    plt.close()
    return word_dict
