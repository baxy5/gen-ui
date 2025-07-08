import React from "react";
import styles from "./styles.module.css";

const DashboardLayoutSystem = () => {
  return (
    <main className="bg-white text-black  w-full h-full">
      <div className={styles.container}>
        <div className={styles.flex}>
          <div className={`${styles.border} ${styles.box_container}`}>
            <h1 className={`${styles.title} ${styles.center_text}`}>
              Kpi Title
            </h1>
            <p className={`${styles.positive} ${styles.center_text}`}>
              +13,45%
            </p>
            <p className={`${styles.description} ${styles.center_text}`}>
              Kpi Description Lorem ipsum dolor sit amet consectetur adipisicing
              elit. Accusantium quaerat asperiores eos facilis maxime maiores
              tempore fuga? Nesciunt, facilis ullam?
            </p>
          </div>
          <div className={`${styles.border} ${styles.box_container}`}>
            <h1 className={`${styles.title} ${styles.center_text}`}>
              Kpi Title
            </h1>
            <p className={`${styles.negative} ${styles.center_text}`}>-9,45%</p>
            <p className={`${styles.description} ${styles.center_text}`}>
              Kpi Description Lorem ipsum dolor sit amet consectetur adipisicing
              elit. Accusantium quaerat asperiores eos facilis maxime maiores
              tempore fuga? Nesciunt, facilis ullam?
            </p>
          </div>
          <div className={`${styles.border} ${styles.box_container}`}>
            <p className={`${styles.information} ${styles.center_text}`}>
              More sales.
            </p>
            <h1 className={`${styles.title} ${styles.center_text}`}>
              Kpi Title
            </h1>
            <p className={`${styles.positive} ${styles.center_text}`}>
              +13,45%
            </p>
            <p className={`${styles.description} ${styles.center_text}`}>
              Kpi Description Lorem ipsum dolor sit amet consectetur adipisicing
              elit. Accusantium quaerat asperiores eos facilis maxime maiores
              tempore fuga? Nesciunt, facilis ullam?
            </p>
          </div>
          <div className={`${styles.border} ${styles.box_container}`}>
            <h1 className={`${styles.title} ${styles.center_text}`}>
              Kpi Title
            </h1>
            <p className={`${styles.negative} ${styles.center_text}`}>-9,45%</p>
            <p className={`${styles.description} ${styles.center_text}`}>
              Kpi Description Lorem ipsum dolor sit amet consectetur adipisicing
              elit. Accusantium quaerat asperiores eos facilis maxime maiores
              tempore fuga? Nesciunt, facilis ullam?
            </p>
          </div>
          <div className={`${styles.border} ${styles.box_container}`}>
            <h1 className={`${styles.title} ${styles.center_text}`}>
              Kpi Title
            </h1>
            <p className={`${styles.negative} ${styles.center_text}`}>-9,45%</p>
            <p className={`${styles.description} ${styles.center_text}`}>
              Kpi Description Lorem ipsum dolor sit amet consectetur adipisicing
              elit. Accusantium quaerat asperiores eos facilis maxime maiores
              tempore fuga? Nesciunt, facilis ullam?
            </p>
            <p className={`${styles.information} ${styles.center_text}`}>
              No more sales.
            </p>
          </div>
        </div>

        <div
          className={`${styles.border} ${styles.default_padding} ${styles.grid}`}
        >
          <h1 className={`${styles.title}`}>Text box title</h1>
          <p className={styles.description}>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Adipisci
            officiis ad fugit debitis vitae id laboriosam eius incidunt? Magnam,
            laborum.
          </p>
        </div>

        <div className={styles.flex}>
          <table className={styles.table}>
            <thead>
              <tr>
                <th>Name</th>
                <th>Value</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Revenue</td>
                <td>$1,234,567</td>
                <td className={styles.table_positive}>Active</td>
              </tr>
              <tr>
                <td>Growth</td>
                <td>+12.5%</td>
                <td className={styles.table_positive}>Positive</td>
              </tr>
              <tr>
                <td>Customers</td>
                <td>1,234</td>
                <td className={styles.table_negative}>Growing</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>
  );
};

export default DashboardLayoutSystem;
