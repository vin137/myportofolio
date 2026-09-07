name : Vincent 

NPM : 2506618540

Kelas : PBP B
### Deskripsi Proyek
Situs web ini merupakan situs web portofolio pribadi untuk **Vincent Armando, mahasiswa S1 Ilmu Komputer Universitas Indonesia**. Website ini dirancang sebagai platform statis yang interaktif untuk memuat identitas akademik, keahlian pemrograman (*skills*), serta rekam jejak organisasi dan kepanitiaan di lingkungan kampus. 

Pengembangan web ini mengusung pendekatan desain modern dengan menerapkan beberapa komponen teknis utama:
*   **HTML5 Semantik murni** (`<header>`, `<main>`, `<section>`, dan `<footer>`) guna memastikan keterbacaan kode (*clean code*) serta aksesibilitas dokumen yang optimal.
*   **Sistem Tata Letak Modern** memanfaatkan *CSS Grid* (`.grid-layout`) dan *Flexbox* (`.row-right`) untuk menciptakan struktur visual asimetris (selang-seling) yang seimbang dan sepenuhnya responsif di layar *desktop* maupun *mobile*.
*   **Fitur Dropdown Tanpa JavaScript** menggunakan elemen bawaan `<details>` dan `<summary>` yang dipadukan dengan animasi CSS `@keyframes` halus untuk menghemat ruang halaman sekaligus meningkatkan pengalaman interaktif pengguna.
*   **Aksen Warna Kebiruan Modern** (*Ice White & Slate Blue*) dipadukan dengan ornamen ilustrasi melayang (*floating vectors*) di area *white space* untuk memperkuat estetika portofolio anak *Computer Science*.

### Instruksi Setup Proyek
Ikuti langkah-langkah berikut untuk menjalankan proyek portofolio ini di lingkungan lokal Anda:

1. **Clone Repository dan Buka Terminal**
   ```bash
   git clone <url-repository-kamu>
   cd myportofolio
   ```

2. **Buat dan Aktifkan Python Virtual Environment**
   * Windows:
     ```bash
     python -m venv env
     .\env\Scripts\activate
     ```
   * macOS/Linux:
     ```bash
     python3 -m venv env
     source env/bin/activate
     ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Migrasikan Database**
   ```bash
   python manage.py migrate
   ```

5. **Jalankan Server Lokal**
   ```bash
   python manage.py runserver
   ```
   Buka [http://127.0.0.1:8000](http://127.0.0.1:8000) di browser Anda.

---

### Tugas 1

### 1. 
> **Pertanyaan:** Apakah Anda menggunakan elemen semantik HTML5 seperti `<section>`, `<article>`, atau `<aside>`? Bagaimana elemen tersebut membantu Anda?

**Ya, saya menggunakan elemen semantik HTML5** seperti `<header>`, `<section>`, dan `<footer>`. Elemen-elemen tersebut sangat membantu saya dalam membangun *static web* karena beberapa alasan:
* **Keterbacaan Kode yang Lebih Baik (*Clean Code*):** Elemen semantik dapat membagi bagian-bagian web menjadi blok-blok dengan aturan fungsi yang jelas dibandingkan jika hanya menggunakan tag `<div>` secara terus-menerus.
* **Kemudahan *Styling* CSS:** Elemen semantik mempermudah pengorganisasian tata letak. Dengan adanya pembagian wilayah yang jelas, saya bisa menerapkan kelas CSS secara global (seperti kelas `.section-block`) tanpa risiko merusak komponen di luar seksi tersebut.

### 2.
> **Pertanyaan:** Tantangan tata letak apa yang Anda temukan? Bagaimana Anda mengevaluasi elemen yang harus diubah posisinya atau diprioritaskan ukurannya?

* **Tantangan Utama:** Tantangan terbesar yang saya hadapi adalah saat menangani elemen yang berukuran kaku (*fixed width*), seperti balok judul seksi yang awalnya terpaku pada ukuran `500px` di tampilan desktop. Ukuran ini membuat komponen melar keluar layar ketika dibuka di perangkat seluler.
* **Strategi Evaluasi:** Saya mengevaluasi struktur *static web* saya dengan mengubah komponen yang bersifat *fixed width* menjadi fleksibel (*fluid*). Ketika dibuka di layar *mobile*, ukurannya otomatis menyesuaikan lebar layar perangkat (`width: 100%`). Selain itu, elemen gambar dan teks yang awalnya tersusun secara horizontal (grid kiri-kanan) di desktop, saya ubah alirannya menjadi susunan vertikal (baris ke bawah) agar tetap nyaman dibaca di layar HP yang sempit.

### 3.
> **Pertanyaan:** Batasan apa yang Anda rasakan pada portofolio Anda? Fungsionalitas dinamis apa yang paling ingin Anda persiapkan pada iterasi selanjutnya?

* **Batasan *Static Web*:** Batasan terbesar yang saya alami berotasi pada **manajemen data yang tidak dinamis**. Setiap kali saya ingin menambah keahlian (*skills*) baru atau riwayat pengalaman baru, saya harus membongkar dan menulis ulang struktur kode HTML secara manual. Jika skala website ini membesar di kemudian hari, risiko terjadinya kesalahan manusia (*human error* seperti salah ketik atau tag rusak) akan semakin tinggi.
* **Iterasi Selanjutnya:** Fungsionalitas dinamis yang paling ingin saya tambahkan di tahap selanjutnya adalah **integrasi dengan database profil**. Dengan adanya sistem basis data pada backend, pengolahan, pembaruan, dan penampilan data portofolio akan berjalan secara otomatis dan jauh lebih efisien.


### AI Disclosure
dalam proyek static web ini, saya menggunakan model gemini untuk membantu menyiapkan blueprint code html dan css. Namun, keterbatasan AI sangat dirasakan saat proses pembuatan static web ini.

### bagian yang dibantu AI
* membantu memperkenalkan beberapa fitur seperti `hover` atau `keyframes`
* membantu memberikan referensi color palette yang cocok.
* membantu dalam memperbaiki struktur code untuk mobile.

### Analisi keterbatasan AI dan perbaikan manual
* masalah struktur padding, margin, dan grid yang awalnya tidak secara akurat menghasilkan hasil yang diharapkan sehingga dibutuhkan tuning manual seperti `align-items: start;`.
* masalah redundant code yang tidak efisien oleh AI sehingga diperlukan strukturisasi ulang secara manual seperti memisahkan `text-left` dan `text-right`, membuat class baru yang lebih generic seperti `box-list`.
* styling yang masih kurang rapi oleh AI sehingga diperlukan stying ulang secara manual seperti penggunaan `grid-layout` dan `@keyframes` yang lebih rapi.