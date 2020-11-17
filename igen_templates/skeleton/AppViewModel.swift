import MGArchitecture
import RxCocoa
import RxSwift

struct AppViewModel {
    let navigator: AppNavigatorType
    let useCase: AppUseCaseType
}

// MARK: - ViewModel
extension AppViewModel: ViewModel {
    struct Input {
        let loadTrigger: Driver<Void>
    }
    
    struct Output {

    }
    
    func transform(_ input: Input, disposeBag: DisposeBag) -> Output {
        return Output()
    }
}
