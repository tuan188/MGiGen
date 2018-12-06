@testable import CleanArchitecture
import XCTest
import RxSwift
import RxBlocking

final class {{ name }}ViewModelTests: XCTestCase {
    private var viewModel: {{ name }}ViewModel!
    private var navigator: {{ name }}NavigatorMock!
    private var useCase: {{ name }}UseCaseMock!
    
    private var input: {{ name }}ViewModel.Input!
    private var output: {{ name }}ViewModel.Output!

    private var disposeBag: DisposeBag!

    private let loadTrigger = PublishSubject<Void>()
    private let reloadTrigger = PublishSubject<Void>()
    private let loadMoreTrigger = PublishSubject<Void>()
    private let select{{ model_name }}Trigger = PublishSubject<IndexPath>()

    override func setUp() {
        super.setUp()
        navigator = {{ name }}NavigatorMock()
        useCase = {{ name }}UseCaseMock()
        viewModel = {{ name }}ViewModel(navigator: navigator, useCase: useCase)
        
        input = {{ name }}ViewModel.Input(
            loadTrigger: loadTrigger.asDriverOnErrorJustComplete(),
            reloadTrigger: reloadTrigger.asDriverOnErrorJustComplete(),
            loadMoreTrigger: loadMoreTrigger.asDriverOnErrorJustComplete(),
            select{{ model_name }}Trigger: select{{ model_name }}Trigger.asDriverOnErrorJustComplete()
        )

        output = viewModel.transform(input)

        disposeBag = DisposeBag()
        
        output.error.drive().disposed(by: disposeBag)
        output.loading.drive().disposed(by: disposeBag)
        output.refreshing.drive().disposed(by: disposeBag)
        output.loadingMore.drive().disposed(by: disposeBag)
        output.fetchItems.drive().disposed(by: disposeBag)
        output.{{ model_variable }}Sections.drive().disposed(by: disposeBag)
        output.selected{{ model_name }}.drive().disposed(by: disposeBag)
        output.isEmptyData.drive().disposed(by: disposeBag)
    }

    func test_loadTrigger_get{{ model_name }}List() {
        // act
        loadTrigger.onNext(())
        let {{ model_variable }}Sections = try? output.{{ model_variable }}Sections.toBlocking(timeout: 1).first()
        
        // assert
        XCTAssert(useCase.get{{ model_name }}List_Called)
        XCTAssertEqual({{ model_variable }}Sections??[0].{{ model_variable }}List.count, 1)
    }

    func test_loadTrigger_get{{ model_name }}List_failedShowError() {
        // arrange
        let get{{ model_name }}List_ReturnValue = PublishSubject<PagingInfo<{{ model_name }}>>()
        useCase.get{{ model_name }}List_ReturnValue = get{{ model_name }}List_ReturnValue

        // act
        loadTrigger.onNext(())
        get{{ model_name }}List_ReturnValue.onError(TestError())
        let error = try? output.error.toBlocking(timeout: 1).first()

        // assert
        XCTAssert(useCase.get{{ model_name }}List_Called)
        XCTAssert(error is TestError)
    }

    func test_reloadTrigger_get{{ model_name }}List() {
        // act
        reloadTrigger.onNext(())
        let {{ model_variable }}Sections = try? output.{{ model_variable }}Sections.toBlocking(timeout: 1).first()

        // assert
        XCTAssert(useCase.get{{ model_name }}List_Called)
        XCTAssertEqual({{ model_variable }}Sections??[0].{{ model_variable }}List.count, 1)
    }

    func test_reloadTrigger_get{{ model_name }}List_failedShowError() {
        // arrange
        let get{{ model_name }}List_ReturnValue = PublishSubject<PagingInfo<{{ model_name }}>>()
        useCase.get{{ model_name }}List_ReturnValue = get{{ model_name }}List_ReturnValue

        // act
        reloadTrigger.onNext(())
        get{{ model_name }}List_ReturnValue.onError(TestError())
        let error = try? output.error.toBlocking(timeout: 1).first()

        // assert
        XCTAssert(useCase.get{{ model_name }}List_Called)
        XCTAssert(error is TestError)
    }

    func test_reloadTrigger_notGet{{ model_name }}ListIfStillLoading() {
        // arrange
        let get{{ model_name }}List_ReturnValue = PublishSubject<PagingInfo<{{ model_name }}>>()
        useCase.get{{ model_name }}List_ReturnValue = get{{ model_name }}List_ReturnValue

        // act
        loadTrigger.onNext(())
        useCase.get{{ model_name }}List_Called = false
        reloadTrigger.onNext(())

        // assert
        XCTAssertFalse(useCase.get{{ model_name }}List_Called)
    }

    func test_reloadTrigger_notGet{{ model_name }}ListIfStillReloading() {
        // arrange
        let get{{ model_name }}List_ReturnValue = PublishSubject<PagingInfo<{{ model_name }}>>()
        useCase.get{{ model_name }}List_ReturnValue = get{{ model_name }}List_ReturnValue

        // act
        reloadTrigger.onNext(())
        useCase.get{{ model_name }}List_Called = false
        reloadTrigger.onNext(())

        // assert
        XCTAssertFalse(useCase.get{{ model_name }}List_Called)
    }

    func test_loadMoreTrigger_loadMore{{ model_name }}List() {
        // act
        loadTrigger.onNext(())
        loadMoreTrigger.onNext(())
        let {{ model_variable }}Sections = try? output.{{ model_variable }}Sections.toBlocking(timeout: 1).first()

        // assert
        XCTAssert(useCase.loadMore{{ model_name }}List_Called)
        XCTAssertEqual({{ model_variable }}Sections??[0].{{ model_variable }}List.count, 2)
    }

    func test_loadMoreTrigger_loadMore{{ model_name }}List_failedShowError() {
        // arrange
        let loadMore{{ model_name }}List_ReturnValue = PublishSubject<PagingInfo<{{ model_name }}>>()
        useCase.loadMore{{ model_name }}List_ReturnValue = loadMore{{ model_name }}List_ReturnValue

        // act
        loadTrigger.onNext(())
        loadMoreTrigger.onNext(())
        loadMore{{ model_name }}List_ReturnValue.onError(TestError())
        let error = try? output.error.toBlocking(timeout: 1).first()

        // assert
        XCTAssert(useCase.loadMore{{ model_name }}List_Called)
        XCTAssert(error is TestError)
    }

    func test_loadMoreTrigger_notLoadMore{{ model_name }}ListIfStillLoading() {
        // arrange
        let get{{ model_name }}List_ReturnValue = PublishSubject<PagingInfo<{{ model_name }}>>()
        useCase.get{{ model_name }}List_ReturnValue = get{{ model_name }}List_ReturnValue

        // act
        loadTrigger.onNext(())
        useCase.get{{ model_name }}List_Called = false
        loadMoreTrigger.onNext(())

        // assert
        XCTAssertFalse(useCase.loadMore{{ model_name }}List_Called)
    }

    func test_loadMoreTrigger_notLoadMore{{ model_name }}ListIfStillReloading() {
        // arrange
        let get{{ model_name }}List_ReturnValue = PublishSubject<PagingInfo<{{ model_name }}>>()
        useCase.get{{ model_name }}List_ReturnValue = get{{ model_name }}List_ReturnValue

        // act
        reloadTrigger.onNext(())
        useCase.get{{ model_name }}List_Called = false
        loadMoreTrigger.onNext(())
        // assert
        XCTAssertFalse(useCase.loadMore{{ model_name }}List_Called)
    }

    func test_loadMoreTrigger_notLoadMoreDocumentTypesStillLoadingMore() {
        // arrange
        let loadMore{{ model_name }}List_ReturnValue = PublishSubject<PagingInfo<{{ model_name }}>>()
        useCase.loadMore{{ model_name }}List_ReturnValue = loadMore{{ model_name }}List_ReturnValue

        // act
        loadMoreTrigger.onNext(())
        useCase.loadMore{{ model_name }}List_Called = false
        loadMoreTrigger.onNext(())

        // assert
        XCTAssertFalse(useCase.loadMore{{ model_name }}List_Called)
    }

    func test_select{{ model_name }}Trigger_to{{ model_name }}Detail() {
        // act
        loadTrigger.onNext(())
        select{{ model_name }}Trigger.onNext(IndexPath(row: 0, section: 0))

        // assert
        XCTAssert(navigator.to{{ model_name }}Detail_Called)
    }
}
