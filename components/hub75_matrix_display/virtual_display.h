#include "matrix_display.h"
// FIXME: this is polluting the global namespace :<
#include "ESP32-HUB75-VirtualMatrixPanel_T.hpp"

namespace esphome
{
    namespace matrix_display
    {
        template <PANEL_CHAIN_TYPE ChainScanType = CHAIN_NONE,
                  PANEL_SCAN_TYPE ScanType = STANDARD_TWO_SCAN,
                  int ScaleFactor = 1>
        class VirtualMatrixDisplay : public MatrixDisplay
        {
        public:
            VirtualMatrixDisplay(uint8_t vmodule_rows, uint8_t vmodule_cols, uint8_t panel_res_x, uint8_t panel_res_y)
                : _vmodule_rows(vmodule_rows), _vmodule_cols(vmodule_cols), _panel_res_x(panel_res_x), _panel_res_y(panel_res_y) {};
            void setup() override
            {
                // Call the base class setup
                MatrixDisplay::setup();

                // Create the virtual display
                this->virtual_display_ = new VirtualMatrixPanel(this->_vmodule_rows, this->_vmodule_rows, this->_panel_res_x, this->_panel_res_y);
                this->virtual_display_->setDisplay(*this->dma_display_);
            }

            /**
             * Fills the entire display with a given color.
             *
             * @param color Color used for filling the entire display
             */
            void fill(Color color) override
            {
                this->virtual_display_->fillScreenRGB888(color.r, color.g, color.b);
            }
            /**
             * Draws a filled rectangle on the display at the given location.
             *
             *
             * @param x1 x-coordinate of the rectangle
             * @param y1 y-coordinate of the rectangle
             * @param width width of the rectangle
             * @param height height of the rectangle
             * @param color Color used for filling the rectangle
             */
            void filled_rectangle(int x1, int y1, int width, int height, Color color = display::COLOR_ON)
            {
                this->virtual_display_->fillRect(x1, y1, width, height, color.r, color.g, color.b);
            }

        private:
            using VirtualMatrixPanel = VirtualMatrixPanel_T<ChainScanType, ScanTypeMapping<ScanType>, ScaleFactor>;
            VirtualMatrixPanel *virtual_display_ = nullptr;

            uint8_t _vmodule_rows = 1;
            uint8_t _vmodule_cols = 1;
            uint8_t _panel_res_x = 0;
            uint8_t _panel_res_y = 0;

            /**
             * Draws a single pixel on the display.
             *
             * @param x x-coordinate of the pixel
             * @param y y-coordinate of the pixel
             * @param color Color of the pixel
             */
            void draw_absolute_pixel_internal(int x, int y, Color color) override
            {
                // Reject invalid pixels
                if (x >= this->_panel_res_x || x < 0 || y >= this->_panel_res_y || y < 0)
                    return;

                // Update pixel value in buffer
                this->virtual_display_->drawPixelRGB888(x, y, color.r, color.g, color.b);
            }
            int get_width_internal() override
            {
                return this->_panel_res_x;
            }
            int get_height_internal() override
            {
                return this->_panel_res_y;
            }
        };
    } // namespace matrix_display
} // namespace esphome