Roundtrip
=========

This tutorial covers some of the basic features of MCL. We will create a simple information model for books that can then be used to describe a certain collection of books.

Creating an information model
-----------------------------

The building blocks for creating information models are in the :py:mod:`pnb.mcl.metamodel.standard` module.

.. note::

    :py:mod:`pnb.mcl.metamodel` is a namespace package that is meant to include alternative metamodel implementations in future (which may be available as, e.g., add-ons to MCL). Alternative implementations will provide additional functionality such as undo-redo support for model changes. As such functionality typically has an impact on performance, it is not provided by the standard implementation. In short: use the standard implementation except if additional functionality is required.
    
A :py:class:`Model <pnb.mcl.metamodel.standard.Model>` is a container for related information. We create a :code:`Model` that will hold our information model for books:

.. execute_code::
    :linenos:
    :scope: roundtrip

    from pnb.mcl.metamodel import standard as mm
    BookML = mm.Model(name='BookML', uri='http://www.plants-and-bytes.de/BookML')
    print(BookML)
    
The :code:`name` a the :code:`Model` should give a hint of what the :code:`Model` is about. Our model will describe 
the *Book Modeling Language*, or :code:`'BookML'`. Most building blocks (i.e., those derived from :py:class:`NamedElement <pnb.mcl.metamodel.standard.NamedElement>`) can have a :code:`name`, and for most of them, the :code:`name` is required.

The :code:`uri` of the :code:`Model` serves as an identifier that should be globally unique. As we (pnb plants & bytes) own the :code:`http://www.plants-and-bytes.de` domain, there is no risk that some other organization will use the same URI by mistake.

.. warning::

    The :code:`uri` of a :code:`Model` is not necessarily a valid web address.
    
    In general, a URI (Uniform Resource Identifier) is just an identifier. In certain settings, it may be useful to actually publish a :code:`Model` under its URI -- which would then be a URL (Uniform Resource Locator). For instance, see Wikipedia for the distinction between `URIs <https://en.wikipedia.org/wiki/Uniform_Resource_Identifier>`_ and `URLs <https://en.wikipedia.org/wiki/URL>`_.

As our information model will cover books, it is straightforward to create a corresponding :py:class:`Class <pnb.mcl.metamodel.standard.Class>`. In our simple model, a :py:class:`ConcreteClass <pnb.mcl.metamodel.standard.ConcreteClass>` shall suffice:

.. execute_code::
    :linenos:
    :scope: roundtrip

    Book = mm.ConcreteClass(name='Book')
    print(Book)

.. todo::

    explain AbstractClass vs. ConcreteClass
    
We can now add the new class to the model:

.. execute_code::
    :linenos:
    :scope: roundtrip

    BookML.add(Book)
    print(Book)

Note that the string representation of :code:`Book` has changed: it knows that it is now part of the model. Vice versa, we can get the :code:`Book` class from the model via its :code:`name`:

.. execute_code::
    :linenos:
    :scope: roundtrip
    
    print(BookML.Book)
    print(Book is BookML.Book)
    
Thus, there is in general no need to keep local names for the elements added to a model.

.. note::

    This namespace concept applies to most classes in the metamodel. For example, also the :py:class:`ConcreteClass <pnb.mcl.metamodel.standard.ConcreteClass>` :code:`BookML.Book` is a namespace that provides access to its sub-elements by name.


.. todo::

    add ref to namespace concept
    
    
To cover the title of a book, we add the following :py:class:`DataProperty <pnb.mcl.metamodel.standard.DataProperty>` to :code:`Book`:

.. execute_code::
    :linenos:
    :scope: roundtrip
   
    BookML.Book.add(mm.DataProperty(
        name='Title', type_=str, lower=1, upper=1))
    print(BookML.Book.Title)

The :code:`type_` of the new :code:`Property` is :code:`str`, the standard Python type for strings. If we give a title for a book, it must be a string; anything else would not be acceptable.  

:code:`lower` and :code:`upper` are the lower and upper limit of the multiplicity of the :code:`Title` :code:`DataProperty`:

- :code:`lower` means that a :code:`Book` must have *at least* 1 value for :code:`Title`;

- :code:`upper` means that a :code:`Book` must have *at most* 1 value for :code:`Title`.

In consequence, a :code:`Book` must have *exactly* 1 value for :code:`Title`.

A :py:class:`DataProperty` is suitable if the :code:`type` of the code:`Property` is a :py:class:`DataType`, including Python's built-in :code:`str`, :code:`int`, and :code:`float`.
