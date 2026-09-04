#include <JaroNGramSearch.h>
#include <Python.h>
#include <vector>
#include <string>


// ============================================================
// Python object
// ============================================================

typedef struct
{
    PyObject_HEAD

    JaroNGramSearch* cpp_object;

} JaroNGramSearchObject;


// ============================================================
// __init__
// ============================================================

static int
JaroNGramSearch_init(
    JaroNGramSearchObject* self,
    PyObject* args,
    PyObject* kwargs
)
{
    int min_N = 1;
    int max_N = 3;
    double N_signif = 1.0;

    static char* keywords[] = {
        (char*)"min_N",
        (char*)"max_N",
        (char*)"N_signif",
        NULL
    };

    if (!PyArg_ParseTupleAndKeywords(
            args,
            kwargs,
            "|iid",
            keywords,
            &min_N,
            &max_N,
            &N_signif))
    {
        return -1;
    }

    self->cpp_object =
        new JaroNGramSearch(
            min_N,
            max_N,
            N_signif
        );

    return 0;
}


// ============================================================
// destructor
// ============================================================

static void
JaroNGramSearch_dealloc(
    JaroNGramSearchObject* self
)
{
    delete self->cpp_object;

    Py_TYPE(self)->tp_free(
        (PyObject*)self
    );
}


// ============================================================
// fit()
// ============================================================

static PyObject*
JaroNGramSearch_fit(
    JaroNGramSearchObject* self,
    PyObject* args
)
{
    PyObject* py_list;

    if (!PyArg_ParseTuple(
            args,
            "O!",
            &PyList_Type,
            &py_list))
    {
        return NULL;
    }

    std::vector<std::string> words;

    Py_ssize_t size =
        PyList_Size(py_list);

    words.reserve(size);

    for (Py_ssize_t i = 0; i < size; ++i)
    {
        PyObject* item =
            PyList_GetItem(
                py_list,
                i
            );

        if (!PyUnicode_Check(item))
        {
            PyErr_SetString(
                PyExc_TypeError,
                "fit() expects list[str]"
            );

            return NULL;
        }

        const char* text =
            PyUnicode_AsUTF8(item);

        if (text == NULL)
        {
            return NULL;
        }

        words.emplace_back(text);
    }

    self->cpp_object->fit(words);

    Py_RETURN_NONE;
}


// ============================================================
// search()
// ============================================================

static PyObject*
JaroNGramSearch_search(
    JaroNGramSearchObject* self,
    PyObject* args
)
{
    const char* query;

    if (!PyArg_ParseTuple(
            args,
            "s",
            &query))
    {
        return NULL;
    }

    // C++ search-ը վերադարձնում է Top-5
    std::array<std::pair<std::string, double>, 5> result =
        self->cpp_object->search(query);

    // Python list՝ 5 արդյունքի համար
    PyObject* py_result =
        PyList_New(result.size());

    if (py_result == NULL)
        return NULL;

    // C++ Top-5 → Python list
    for (size_t i = 0; i < result.size(); ++i)
    {
        PyObject* item =
            PyTuple_New(2);

        if (item == NULL)
        {
            Py_DECREF(py_result);
            return NULL;
        }

        // word
        PyObject* py_word =
            PyUnicode_FromString(
                result[i].first.c_str()
            );

        // score
        PyObject* py_score =
            PyFloat_FromDouble(
                result[i].second
            );

        if (py_word == NULL ||
            py_score == NULL)
        {
            Py_XDECREF(py_word);
            Py_XDECREF(py_score);

            Py_DECREF(item);
            Py_DECREF(py_result);

            return NULL;
        }

        // tuple = (word, score)
        PyTuple_SetItem(
            item,
            0,
            py_word
        );

        PyTuple_SetItem(
            item,
            1,
            py_score
        );

        // list[i] = (word, score)
        PyList_SetItem(
            py_result,
            i,
            item
        );
    }

    return py_result;
}


// ============================================================
// FinalWordsData property
// ============================================================

static PyObject*
JaroNGramSearch_get_FinalWordsData(
    JaroNGramSearchObject* self,
    void* closure
)



{
    const auto& final_words_data =
        self->cpp_object->FinalWordsData;

    PyObject* py_words =
        PyList_New(final_words_data.size());

    if (py_words == nullptr)
        return nullptr;

    for (size_t i = 0; i < final_words_data.size(); ++i)
    {
        const auto& word_data =
            final_words_data[i];

        // ----------------------------------------------------
        // word
        // ----------------------------------------------------

        PyObject* py_word =
            PyUnicode_FromString(
                word_data.word.c_str()
            );

        if (py_word == nullptr)
        {
            Py_DECREF(py_words);
            return nullptr;
        }

        // ----------------------------------------------------
        // count_term
        // ----------------------------------------------------

        PyObject* py_count_term =
            PyLong_FromLong(
                word_data.count_term
            );

        if (py_count_term == nullptr)
        {
            Py_DECREF(py_word);
            Py_DECREF(py_words);
            return nullptr;
        }

        // ----------------------------------------------------
        // ngrams
        // ----------------------------------------------------

        PyObject* py_ngrams =
            PyList_New(
                word_data.ngrams.size()
            );

        if (py_ngrams == nullptr)
        {
            Py_DECREF(py_count_term);
            Py_DECREF(py_word);
            Py_DECREF(py_words);
            return nullptr;
        }

        for (size_t j = 0;
             j < word_data.ngrams.size();
             ++j)
        {
            const auto& ngram =
                word_data.ngrams[j];

            PyObject* py_item =
                PyTuple_New(3);

            if (py_item == nullptr)
            {
                Py_DECREF(py_ngrams);
                Py_DECREF(py_count_term);
                Py_DECREF(py_word);
                Py_DECREF(py_words);
                return nullptr;
            }

            // index
            PyObject* py_index =
                PyLong_FromLong(
                    ngram.index
                );

            // tfidf
            PyObject* py_tfidf =
                PyFloat_FromDouble(
                    ngram.tfidf
                );

            // positions
            PyObject* py_positions =
                PyList_New(
                    ngram.positions.size()
                );

            if (py_index == nullptr ||
                py_tfidf == nullptr ||
                py_positions == nullptr)
            {
                Py_XDECREF(py_index);
                Py_XDECREF(py_tfidf);
                Py_XDECREF(py_positions);

                Py_DECREF(py_item);
                Py_DECREF(py_ngrams);
                Py_DECREF(py_count_term);
                Py_DECREF(py_word);
                Py_DECREF(py_words);

                return nullptr;
            }

            // ------------------------------------------------
            // positions
            // ------------------------------------------------

            for (size_t k = 0;
                 k < ngram.positions.size();
                 ++k)
            {
                PyObject* position =
                    PyLong_FromLong(
                        ngram.positions[k]
                    );

                if (position == nullptr)
                {
                    Py_DECREF(py_index);
                    Py_DECREF(py_tfidf);
                    Py_DECREF(py_positions);

                    Py_DECREF(py_item);
                    Py_DECREF(py_ngrams);
                    Py_DECREF(py_count_term);
                    Py_DECREF(py_word);
                    Py_DECREF(py_words);

                    return nullptr;
                }

                // PyList_SetItem steals reference
                PyList_SetItem(
                    py_positions,
                    k,
                    position
                );
            }

            // ------------------------------------------------
            // (index, tfidf, positions)
            // ------------------------------------------------

            // PyTuple_SetItem steals references
            PyTuple_SetItem(
                py_item,
                0,
                py_index
            );

            PyTuple_SetItem(
                py_item,
                1,
                py_tfidf
            );

            PyTuple_SetItem(
                py_item,
                2,
                py_positions
            );

            // PyList_SetItem steals reference
            PyList_SetItem(
                py_ngrams,
                j,
                py_item
            );
        }

        // ----------------------------------------------------
        // (word, count_term, ngrams)
        // ----------------------------------------------------

        PyObject* py_word_data =
            PyTuple_New(3);

        if (py_word_data == nullptr)
        {
            Py_DECREF(py_ngrams);
            Py_DECREF(py_count_term);
            Py_DECREF(py_word);
            Py_DECREF(py_words);

            return nullptr;
        }

        // PyTuple_SetItem steals references
        PyTuple_SetItem(
            py_word_data,
            0,
            py_word
        );

        PyTuple_SetItem(
            py_word_data,
            1,
            py_count_term
        );

        PyTuple_SetItem(
            py_word_data,
            2,
            py_ngrams
        );

        // PyList_SetItem steals reference
        PyList_SetItem(
            py_words,
            i,
            py_word_data
        );
    }

    return py_words;
}

// ============================================================
// Python get/set definitions
// ============================================================

static PyGetSetDef JaroNGramSearch_getset[] =
{
    {
        (char*)"FinalWordsData",
        (getter)JaroNGramSearch_get_FinalWordsData,
        NULL,
        (char*)"Training words data",
        NULL
    },

    {NULL, NULL, NULL, NULL, NULL}
};


// ============================================================
// Python methods
// ============================================================

static PyMethodDef JaroNGramSearch_methods[] =
{
    {
        "fit",
        (PyCFunction)JaroNGramSearch_fit,
        METH_VARARGS,
        "Fit model with list of words"
    },

    {
        "search",
        (PyCFunction)JaroNGramSearch_search,
        METH_VARARGS,
        "Search similar words"
    },

    {NULL, NULL, 0, NULL}
};


// ============================================================
// Python type
// ============================================================

static PyTypeObject JaroNGramSearchType =
{
    PyVarObject_HEAD_INIT(NULL, 0)

    .tp_name =
        "my_module.JaroNGramSearch",

    .tp_basicsize =
        sizeof(JaroNGramSearchObject),

    .tp_dealloc =
        (destructor)JaroNGramSearch_dealloc,

    .tp_flags =
        Py_TPFLAGS_DEFAULT,

    .tp_doc =
        "JaroNGramSearch",

    .tp_methods =
        JaroNGramSearch_methods,

    .tp_getset =
        JaroNGramSearch_getset,

    .tp_init =
        (initproc)JaroNGramSearch_init,

    .tp_new =
        PyType_GenericNew,
};


// ============================================================
// Module
// ============================================================

static PyModuleDef module =
{
    PyModuleDef_HEAD_INIT,

    "my_module",

    "C++ NGram Search",

    -1,

    NULL
};


// ============================================================
// Module initialization
// ============================================================

PyMODINIT_FUNC
PyInit_my_module(void)
{
    if (PyType_Ready(
            &JaroNGramSearchType
        ) < 0)
    {
        return NULL;
    }

    PyObject* m =
        PyModule_Create(&module);

    if (m == NULL)
        return NULL;

    Py_INCREF(
        &JaroNGramSearchType
    );

    if (PyModule_AddObject(
            m,
            "JaroNGramSearch",
            (PyObject*)&JaroNGramSearchType
        ) < 0)
    {
        Py_DECREF(
            &JaroNGramSearchType
        );

        Py_DECREF(m);

        return NULL;
    }

    return m;
}