import MGArchitecture
import MGLoadMore
import Reusable
import RxCocoa
import RxSwift
import Then
import UIKit

final class {{ name }}ViewController: UIViewController, Bindable {

    // MARK: - IBOutlets

    @IBOutlet weak var collectionView: PagingCollectionView!

    // MARK: - Properties

    var viewModel: {{ name }}ViewModel!
    var disposeBag = DisposeBag()
    
    private var {{ model_variable }}Sections = [{{ name }}ViewModel.{{ model_name }}SectionViewModel]()

    struct LayoutOptions {
        var itemSpacing: CGFloat = 16
        var lineSpacing: CGFloat = 16
        var itemsPerRow: Int = 2

        var sectionInsets = UIEdgeInsets(
            top: 16.0,
            left: 16.0,
            bottom: 16.0,
            right: 16.0
        )

        var itemSize: CGSize {
            let screenSize = UIScreen.main.bounds

            let paddingSpace = sectionInsets.left
                + sectionInsets.right
                + CGFloat(itemsPerRow - 1) * itemSpacing

            let availableWidth = screenSize.width - paddingSpace
            let widthPerItem = availableWidth / CGFloat(itemsPerRow)
            let heightPerItem = widthPerItem

            return CGSize(width: widthPerItem, height: heightPerItem)
        }
    }

    private var layoutOptions = LayoutOptions()

    // MARK: - Life Cycle

    override func viewDidLoad() {
        super.viewDidLoad()
        configView()
    }

    deinit {
        logDeinit()
    }

    // MARK: - Methods

    private func configView() {
        collectionView.do {
            $0.register(cellType: {{ model_name }}Cell.self)
            $0.register(supplementaryViewType: {{ model_name }}HeaderView.self, 
                        ofKind: UICollectionView.elementKindSectionHeader)
            $0.delegate = self
            $0.dataSource = self
            $0.prefetchDataSource = self
            $0.alwaysBounceVertical = true
            {% if not paging %}
            $0.refreshFooter = nil
            {% endif %}
        }
    }

    func bindViewModel() {
        let input = {{ name }}ViewModel.Input(
            loadTrigger: Driver.just(()),
            reloadTrigger: collectionView.refreshTrigger,
            {% if paging %}
            loadMoreTrigger: collectionView.loadMoreTrigger,
            {% endif %}
            select{{ model_name }}Trigger: collectionView.rx.itemSelected.asDriver()
        )

        let output = viewModel.transform(input, disposeBag: disposeBag)

        output.${{ model_variable }}Sections
            .asDriver()
            .drive(onNext: { [unowned self] sections in
                self.{{ model_variable }}Sections = sections
                self.collectionView.reloadData()
            })
            .disposed(by: disposeBag)

        output.$error
            .asDriver()
            .unwrap()
            .drive(rx.error)
            .disposed(by: disposeBag)

        output.$isLoading
            .asDriver()
            .drive(rx.isLoading)
            .disposed(by: disposeBag)

        output.$isReloading
            .asDriver()
            .drive(collectionView.isRefreshing)
            .disposed(by: disposeBag)

        {% if paging %}
        output.$isLoadingMore
            .asDriver()
            .drive(collectionView.isLoadingMore)
            .disposed(by: disposeBag)

        {% endif %}
        output.$isEmpty
            .asDriver()
            .drive()
            .disposed(by: disposeBag)
    }
}

// MARK: - Binders
extension {{ name }}ViewController {

}

// MARK: - UICollectionViewDelegate
extension {{ name }}ViewController: UICollectionViewDelegate, UICollectionViewDelegateFlowLayout {
    func collectionView(_ collectionView: UICollectionView,
                        layout collectionViewLayout: UICollectionViewLayout,
                        sizeForItemAt indexPath: IndexPath) -> CGSize {
        // Set Collection View's Estimate Size to None in Storyboard
        return layoutOptions.itemSize
    }

    func collectionView(_ collectionView: UICollectionView,
                        layout collectionViewLayout: UICollectionViewLayout,
                        insetForSectionAt section: Int) -> UIEdgeInsets {
        return layoutOptions.sectionInsets
    }

    func collectionView(_ collectionView: UICollectionView,
                        layout collectionViewLayout: UICollectionViewLayout,
                        minimumLineSpacingForSectionAt section: Int) -> CGFloat {
        return layoutOptions.lineSpacing
    }

    func collectionView(_ collectionView: UICollectionView,
                        layout collectionViewLayout: UICollectionViewLayout,
                        minimumInteritemSpacingForSectionAt section: Int) -> CGFloat {
        return layoutOptions.itemSpacing
    }

    func collectionView(_ collectionView: UICollectionView,
                        layout collectionViewLayout: UICollectionViewLayout,
                        referenceSizeForHeaderInSection section: Int) -> CGSize {
        return CGSize(width: collectionView.bounds.width, height: 44)
    }
}

// MARK: - UICollectionViewDataSource
extension {{ name }}ViewController: UICollectionViewDataSource {
    func numberOfSections(in collectionView: UICollectionView) -> Int {
        return {{ model_variable }}Sections.count
    }
    
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        return {{ model_variable }}Sections[section].{{ model_variable }}List.count
    }
    
    func collectionView(_ collectionView: UICollectionView,
                        cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        let {{ model_variable }} = {{ model_variable }}Sections[indexPath.section].{{ model_variable }}List[indexPath.row]
        
        return collectionView.dequeueReusableCell(for: indexPath, cellType: {{ model_name }}Cell.self)
            .then {
                $0.bindViewModel({{ model_variable }})
            }
    }
    
    func collectionView(_ collectionView: UICollectionView,
                        viewForSupplementaryElementOfKind kind: String,
                        at indexPath: IndexPath) -> UICollectionReusableView {
        let section = {{ model_variable }}Sections[indexPath.section]
        
        return collectionView.dequeueReusableSupplementaryView(ofKind: UICollectionView.elementKindSectionHeader,
                                                               for: indexPath,
                                                               viewType: {{ model_name }}HeaderView.self)
            .then {
                $0.titleLabel.text = section.header
            }
    }
}

// MARK: - StoryboardSceneBased
extension {{ name }}ViewController: StoryboardSceneBased {
    static var sceneStoryboard = UIStoryboard()
}

// MARK: - UICollectionViewDataSourcePrefetching
extension {{ name }}ViewController: UICollectionViewDataSourcePrefetching {
    func collectionView(_ collectionView: UICollectionView, prefetchItemsAt indexPaths: [IndexPath]) {

    }
    
    func collectionView(_ collectionView: UICollectionView, cancelPrefetchingForItemsAt indexPaths: [IndexPath]) {
        
    }
}
