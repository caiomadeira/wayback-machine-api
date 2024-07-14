#include<stdio.h>
#include<stdlib.h>
#include<string.h>

#define TARGET_1 "=\"/web/"
#define ARCHIVE_LINK "https://web.archive.org"

#define MALLOC_ERR(msg) printf(msg); return 3
#define OPENFILE_ERR(msg) printf(msg); return 2
#define GENERIC_ERR(msg) printf(msg); return 1

int raise(int status)
{   
    int code;
    switch (status)
    {
    case 2:
        code = OPENFILE_ERR("OPENFILE_ERR: Couldnt open the file. Check the filename or mode...\n");
        exit(code);
    case 3:
        code = MALLOC_ERR("MALLOC_ERR: The variable allocated returned NULL.\n");
        exit(code);
    default:
        code = GENERIC_ERR("GENERIC_ERR: Something wrong happen. Exiting...\n");
        exit(code);
    }
}

FILE* openfile(const char* filename, const char* mode) {
    FILE* fp = fopen(filename, mode);
    if (fp == NULL) {
        perror("Error opening file");
        exit(EXIT_FAILURE);
    }
    return fp;
}

char* allocstr(size_t size) {
    char* buffer = (char*)malloc((size + 1) * sizeof(char)); // +1 para o caractere nulo
    if (buffer == NULL) {
        perror("Error allocating memory");
        exit(EXIT_FAILURE);
    }
    buffer[0] = '\0'; // Inicializar a string com caractere nulo
    return buffer;
}

void printcharvec(char** v, int n) {
    for (int i = 0; i < n; i++) {
        if (v[i] != NULL && v[i][0] != '\0') {
            printf("%s\n", v[i]);
        }
    }
}

char** alloccharvec(int n) {
    char** buffer = (char**)malloc(n * sizeof(char*));
    if (buffer != NULL) {
        for (int i = 0; i < n; i++) {
            buffer[i] = allocstr(n / 2);
            if (buffer[i] == NULL) {
                for (int j = 0; j < i; j++) {
                    free(buffer[j]);
                }
                free(buffer);
                return NULL;
            }
        }
    }
    else {
        perror("Error allocating memory");
        exit(EXIT_FAILURE);
    }
    return buffer;
}

static char* parsestr(char* s)
{
    int concatstrlen = (int)strlen(ARCHIVE_LINK);

    for (int i = 0; i < (int)strlen(s); i++)
    {
        char* quote = strchr(s + i, '"');
        if (quote != NULL)
        {
            int quote_index = (quote + 1) - s;
            char* newstr = allocstr((int)strlen(s) + concatstrlen + 1);

            strncpy(newstr, s, quote_index); // Copia a parte da string até o "
            newstr[quote_index] = '\0';
            strcat(newstr, ARCHIVE_LINK); // Concatena a string adicional
            strcat(newstr, s + quote_index); // Concatena o restante da string original a partir do "
            return newstr;
        }
    }
    return s;
}

void readnwrite(FILE* fin, FILE* fout, char** content, int content_size) {
    char* lines = allocstr(400); // Alocação de 400 caracteres
    int line_count = 0;
    while (fgets(lines, 400, fin) != NULL && line_count < content_size) { // Use fgets para ler uma linha inteira
        if (strstr(lines, TARGET_1) != NULL) 
        {
            strcpy(content[line_count], lines);
            char* parsed_line = parsestr(lines);
            printf("%s\n", parsed_line);
            fprintf(fout, "%s", parsed_line);

            line_count++;
        }
        else
        {
            fprintf(fout, "%s\n", lines);
        }
    }
    free(lines);
}

int init_htmlparse(const char * pathin, const char * pathout, int nbuffer)
{
    // check path
    if (pathin != NULL && pathout != NULL && nbuffer >= 200)
    {
        char** content = alloccharvec(nbuffer);
        if (content != NULL) {
            FILE* fin = openfile(pathin, "r"); // Abra o arquivo em modo de leitura
            FILE* fout = openfile(pathout, "w"); // Abra o arquivo em modo de gravacao

            readnwrite(fin, fout, content, nbuffer);
            fclose(fin); // Fechar o arquivo
            return 1;
        }
    }
    return 0;
}


int main(void)
{
    const char* pathIn = "D:/GitHub/wayback-machine-api/tmp/index.html";
    const char* pathOut = "D:/GitHub/wayback-machine-api/tmp/index_parsed.html";
    int nbuffer = 400;
    int result = init_htmlparse(pathIn, pathOut, nbuffer);
    if (result != 0)
        printf("Sucess\n");
    else
        printf("Fail\n");

    return 0;
}