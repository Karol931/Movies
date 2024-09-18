import '../../assets/styles.css'
import NavBar from '../../components/NavBar';
import SearchBox from '../../components/SearchBox';

const HomePage = () => {
    return (
        <div className="App">
            <NavBar />
            <main className="main-content">
                <div className="search-section">
                    <h2>Movies2watch.tv</h2>
                    <SearchBox />
                </div>
            </main>
        </div>
    );
}

export default HomePage