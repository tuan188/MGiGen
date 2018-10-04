protocol {{ name }}UseCaseType {
    func get{{ model_name }}List() -> Observable<PagingInfo<{{ model_name }}>>
    func loadMore{{ model_name }}List(page: Int) -> Observable<PagingInfo<{{ model_name }}>>
}

struct {{ name }}UseCase: {{ name }}UseCaseType {
    func get{{ model_name }}List() -> Observable<PagingInfo<{{ model_name }}>> {
        return loadMore{{ model_name }}List(page: 1)
    }
    
    func loadMore{{ model_name }}List(page: Int) -> Observable<PagingInfo<{{ model_name }}>> {
        return Observable.empty()
    }
}
