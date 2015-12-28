#ifndef ARRAYALLOC_HH_
#define ARRAYALLOC_HH_

inline void* operator new(size_t, void* ptr) throw()
{
	return ptr;
}

template<int NUM, class T>
class ArrayAlloc
{
public:
	template <class U>
	ArrayAlloc(const U& init)
	{
		for (int i = 0; i < NUM; i++)
			new ((void*)((T*) items + i)) T(init(i));
	}
	~ArrayAlloc()
	{
		for (int i = 0; i < NUM; i++)
			((T*) items + i)->~T();
	}

	inline T& operator[](int i)
	{
		return *((T*) items + i);
	}
	inline const T& operator[](int i) const
	{
		return *((const T*) items + i);
	}

private:
	ArrayAlloc(const ArrayAlloc&) {}
	ArrayAlloc& operator=(const ArrayAlloc&) { return *this; }
	char items[NUM * sizeof(T)];
};

#endif /* ARRAYALLOC_HH_ */
