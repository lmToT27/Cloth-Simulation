# Mô phỏng vải lưới

<p align="center">
  <a href="./README.md">English</a> &nbsp;|&nbsp; <b>Tiếng Việt</b>
</p>

Dự án này triển khai một mô phỏng vật lý của một lưới (vải/lưới) sử dụng **Hệ thống Lò xo-Khối lượng (Mass-Spring System)** và **Tích phân Verlet (Verlet Integration)**. Mô phỏng này mô hình hóa hành vi vật lý của các vật liệu có thể biến dạng bằng cách coi chúng như một mạng lưới các điểm khối lượng được kết nối bởi các lò xo ảo.

## 1. Cơ sở lý thuyết: Hệ thống Khối lượng - Lò xo

Mô hình này coi vật thể là một lưới các điểm chất lượng (mass points) được nối với nhau bằng các lò xo ảo không trọng lượng.

### Cấu trúc lưới (Grid Topology)

Để mô phỏng một tấm vải hoặc lưới có hành vi thực tế, chúng ta không chỉ nối các điểm liền kề. Cần có 3 loại lò xo:

1. **Structural Springs (Lò xo cấu trúc):** Nối các điểm lân cận (ngang/dọc). Chịu lực kéo/nén chính.
    
2. **Shear Springs (Lò xo trượt/cắt):** Nối các điểm theo đường chéo. Ngăn lưới bị biến dạng xiên (bị méo).
    
3. **Bend Springs (Lò xo uốn):** Nối các điểm cách nhau 1 điểm (nhảy cóc). Ngăn lưới bị gập lại quá dễ dàng, tạo độ cứng cho vật liệu.
    

### Lực đàn hồi (Hooke's Law)

Lực tác dụng giữa hai điểm $P_1$ và $P_2$ được tính theo định luật Hooke:

$$\vec{F}_s = k \cdot (|\vec{L}| - R) \cdot \frac{\vec{L}}{|\vec{L}|}$$

Trong đó:

- $k$: Hệ số đàn hồi (stiffness).
    
- $\vec{L} = P_2 - P_1$: Vector khoảng cách giữa 2 điểm.
    
- $|\vec{L}|$: Khoảng cách hiện tại.
    
- $R$: Chiều dài nghỉ (rest length) của lò xo.
    
- $\frac{\vec{L}}{|\vec{L}|}$: Vector đơn vị hướng lực.
    

---

## 2. Thuật toán tích phân Verlet (Verlet Integration)

Tại sao lại dùng Verlet thay vì Euler?

- **Euler ($v = v + a \cdot dt; p = p + v \cdot dt$):** Kém ổn định, năng lượng tăng dần theo thời gian (vật thể bị nổ/bay mất nếu $dt$ lớn).
    
- **Verlet:** Tính vị trí mới dựa trên vị trí hiện tại và vị trí _ngay trước đó_. Nó bảo toàn năng lượng tốt hơn và tự động xử lý vận tốc mà không cần lưu trữ biến vận tốc tường minh.
    

Công thức cập nhật vị trí cơ bản:

$$\vec{x}_{new} = 2\vec{x}_{curr} - \vec{x}_{prev} + \vec{a} \cdot \Delta t^2$$

Trong đó gia tốc $\vec{a} = \frac{\vec{F}}{m}$.

---

## 3. Quy trình Mô phỏng (Simulation Loop)

Để triển khai nâng cao, chúng ta thường thực hiện theo các bước sau trong mỗi khung hình (frame):

1. **Tích lũy lực (Accumulate Forces):**
    
    - Reset lực về 0.
        
    - Cộng lực trọng trường: $\vec{F} += m \cdot \vec{g}$.
        
    - Duyệt qua tất cả các lò xo, tính lực đàn hồi (Hooke) và cộng vào 2 đầu mút.
        
    - _Lưu ý:_ Có thể thêm lực cản không khí (Damping) để hệ thống không dao động mãi mãi.
        
2. **Tích phân Verlet (Integrate):**
    
    - Với mỗi điểm, cập nhật vị trí theo công thức Verlet.
        
3. **Thỏa mãn ràng buộc (Constraints Solving):**
    
    - Đây là bước quan trọng để giữ lưới ổn định.
        
    - **Pinning:** Giữ cố định một số điểm (ví dụ: treo tấm vải lên).
        
    - **Collision:** Kiểm tra nếu điểm chạm đất hoặc vật cản, đẩy nó ra ngoài.
        
    - _(Nâng cao)_ **Stick Constraint:** Đôi khi thay vì dùng lực lò xo (vốn mềm và đàn hồi), người ta dùng ràng buộc khoảng cách cứng (Distance Constraint) và giải bằng phương pháp lặp (Relaxation) để vải không bị dãn vô hạn.
