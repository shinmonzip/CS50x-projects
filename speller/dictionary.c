#include "dictionary.h"
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

// Representa um nó na tabela hash
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Número de "buckets" na tabela hash
const unsigned int TABLE_SIZE = 50000;

// Tabela hash
node *table[TABLE_SIZE];

// Contador para o número de palavras no dicionário
int counter = 0;

// Função hash
unsigned int hash(const char *word)
{
    unsigned int hashvalue = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        hashvalue += tolower(word[i]);
        hashvalue = (hashvalue * tolower(word[i])) % TABLE_SIZE;
    }
    return hashvalue;
}

// Função que carrega o dicionário na memória
bool load(const char *dictionary)
{
    // Abre o arquivo do dicionário
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        fprintf(stderr, "Erro ao abrir o arquivo do dicionário.\n");
        return false;
    }

    // Buffer para armazenar a palavra atual
    char wordlist[LENGTH + 1];
    while (fscanf(file, "%s", wordlist) != EOF)
    {
        // Conta o número de palavras carregadas
        counter++;

        // Aloca memória para o novo nó
        node *newNode = malloc(sizeof(node));
        if (newNode == NULL)
        {
            return false;
        }

        // Copia a palavra para o novo nó
        strcpy(newNode->word, wordlist);
        newNode->next = NULL;

        // Calcula o índice do hash para a palavra
        int index = hash(wordlist);

        // Se a posição na tabela está vazia, insere a palavra
        if (table[index] == NULL)
        {
            table[index] = newNode;
        }
        else
        {
            // Se já existe um nó, insere o novo nó no início da lista
            newNode->next = table[index];
            table[index] = newNode;
        }
    }
    fclose(file);
    return true;
}

// Função que verifica se uma palavra está no dicionário
bool check(const char *word)
{
    // Calcula o índice do hash para a palavra
    int index = hash(word);

    // Percorre a lista encadeada na posição calculada
    node *cursor = table[index];
    while (cursor != NULL)
    {
        // Compara a palavra sem considerar maiúsculas/minúsculas
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Função que retorna o número de palavras no dicionário
unsigned int size(void)
{
    return counter;
}

// Função que descarrega a memória utilizada pelo dicionário
bool unload(void)
{
    // Libera a memória de cada nó na tabela hash
    node *cursor, *temp;
    for (int i = 0; i < TABLE_SIZE; i++)
    {
        cursor = table[i];
        while (cursor != NULL)
        {
            temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    return true;
}
