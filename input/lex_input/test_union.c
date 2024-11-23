
union my_union1 {

int value;
float weight;
} u1, u2;


union my_union2 {

int value;

union my_union1 my_union;

struct my_struct1 my_struct;
} u;

union my_union3 {

int value;
char id;
};